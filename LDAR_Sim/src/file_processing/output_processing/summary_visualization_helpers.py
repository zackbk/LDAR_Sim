"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        summary_visualization_helpers.py
Purpose: Contains functions to help with the summary visualizations.

This program is free software: you can redistribute it and/or modify
it under the terms of the MIT License as published
by the Free Software Foundation, version 3.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
MIT License for more details.
You should have received a copy of the MIT License
along with this program.  If not, see <https://opensource.org/licenses/MIT>.

------------------------------------------------------------------------------
"""

from matplotlib import lines, pyplot as plt, ticker
import scipy.stats
from constants import output_file_constants
import seaborn as sns
from typing import Any, Tuple, Union
import numpy as np
import re


def get_non_baseline_prog_names(emis_summary_info, baseline_program) -> list:
    return [
        program_name
        for program_name in emis_summary_info[
            output_file_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.PROG_NAME
        ].unique()
        if program_name != baseline_program
    ]


def format_tick_labels_with_metric_prefix(x, pos):
    """
    Function to format tick labels as words with metric prefixes
    """
    if abs(x) < 1:
        return "{:.1f}".format(x)
    powers = [18, 15, 12, 9, 6, 3, 0]
    label = ["H", "Q", "T", "B", "M", "K", ""]
    for i, power in enumerate(powers):
        if abs(x) >= 10**power:
            return "{:.1f}{}".format(x / 10**power, label[i])


def plot_hist_percent_occurrence_with_smoothed_curved(
    legend_elements: list,
    ax: plt.Axes,
    x_values: list,
    program_name: str,
    color: Tuple[float, float, float],
    bin_range: Tuple[float, float],
    x_label: str,
    y_label: str,
    legend_label: str = None,
    bin_width: float = 0,
    bins: Union[int, str] = "auto",
    x_locator: ticker.Locator = ticker.AutoLocator(),
    y_locator: ticker.Locator = ticker.MaxNLocator(nbins="auto", integer=True, prune=None),
):
    if bin_width != 0:
        sns.histplot(
            x_values,
            kde=True,
            color=color,
            element="step",
            ax=ax,
            binwidth=bin_width,
            binrange=bin_range,
            stat="percent",
        )
    else:
        sns.histplot(
            x_values,
            kde=True,
            color=color,
            element="step",
            ax=ax,
            binrange=bin_range,
            bins=bins,
            stat="percent",
        )

    legend_elements.append(
        lines.Line2D(
            [0],
            [0],
            color=color,
            label=legend_label if legend_label else program_name,
            markerfacecolor=color,
            markersize=15,
        )
    )
    if x_label and y_label:
        ax.set(
            xlabel=x_label,
            ylabel=y_label,
        )

    ax.xaxis.set_major_locator(locator=x_locator)
    ax.yaxis.set_major_locator(locator=y_locator)

    # Set custom formatter for x-axis
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(format_tick_labels_with_metric_prefix))


def gen_annual_emissions_summary_list(
    emis_summary_info, program_names
) -> dict[str, Tuple[list[float], list[float]]]:

    t_ann_columns = sorted(
        [
            column
            for column in emis_summary_info.columns
            if re.match(
                output_file_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.REGX_T_ANN_EMIS, column
            )
        ]
    )
    est_ann_columns = sorted(
        [
            column
            for column in emis_summary_info.columns
            if re.match(
                output_file_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.REGX_EST_ANN_EMIS, column
            )
        ]
    )

    # remove the first year "spin up" column if simulation is long enough
    # TODO: update this logic with spin up changes...
    if len(t_ann_columns) > 1:
        t_ann_columns = t_ann_columns[1:]
    if len(est_ann_columns) > 1:
        est_ann_columns = est_ann_columns[1:]

    paired_emissions_lists = {}

    for program_name in program_names:
        true_emis_list = np.ravel(
            emis_summary_info.loc[
                emis_summary_info[output_file_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.PROG_NAME]
                == program_name,
                t_ann_columns,
            ].values
        ).tolist()

        est_emis_list = np.ravel(
            emis_summary_info.loc[
                emis_summary_info[output_file_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.PROG_NAME]
                == program_name,
                est_ann_columns,
            ].values
        ).tolist()

        paired_emissions_lists[program_name] = (true_emis_list, est_emis_list)
    return paired_emissions_lists


def gen_annual_mitigation_summary_list(
    emis_summary_info, program_names
) -> dict[str, Tuple[list[float], list[float]]]:

    mit_ann_columns = sorted(
        [
            column
            for column in emis_summary_info.columns
            if re.match(output_file_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.REGX_T_ANN_MIT, column)
        ]
    )

    # remove the first year "spin up" column if simulation is long enough
    # TODO: update this logic with spin up changes...
    if len(mit_ann_columns) > 1:
        mit_ann_columns = mit_ann_columns[1:]

    annual_mitigation_lists = {}
    is_there_mitigation = False
    for program_name in program_names:
        mitigation_list = np.ravel(
            emis_summary_info.loc[
                emis_summary_info[output_file_constants.EMIS_SUMMARY_COLUMNS_ACCESSORS.PROG_NAME]
                == program_name,
                mit_ann_columns,
            ].values
        ).tolist()
        # Check if there is any mitigation in the program only
        # if there has not been any mitigation found yet
        if not is_there_mitigation:
            is_there_mitigation = is_list_non_zero(mitigation_list)
        annual_mitigation_lists[program_name] = mitigation_list
    # If there is mitigation, return the mitigation lists
    if is_there_mitigation:
        return annual_mitigation_lists
    else:
        # Return none if there is no mitigation in any program
        return None


def is_list_non_zero(list) -> bool:
    return all(item != 0 for item in list)


def gen_true_estimated_annualized_statistics(
    stat_function: callable, paired_emissions_lists: dict
) -> dict:

    program_stat_lists: dict = {}

    for program, (t_total_emis, est_total_emis) in paired_emissions_lists.items():
        percent_diff = [stat_function(est, true) for est, true in zip(est_total_emis, t_total_emis)]
        program_stat_lists[program] = percent_diff

    return program_stat_lists


def calculate_histogram_bin_range(
    program_hist_stats: dict[str, list[float]],
    histogram_properties: dict[str, Any],
    hist_stats_accessor: int,
) -> Tuple[float, float]:
    if "bin_range" in histogram_properties and histogram_properties["bin_range"][1] is None:
        max_val: float = max(
            max([max(stat[hist_stats_accessor]) for stat in program_hist_stats.values()]),
            float("-inf"),
        )
    else:
        max_val: float = histogram_properties["bin_range"][1]

    if "bin_range" in histogram_properties and histogram_properties["bin_range"][0] is None:
        min_val: float = min(
            min([min(stat[hist_stats_accessor]) for stat in program_hist_stats.values()]),
            float("inf"),
        )
    else:
        min_val: float = histogram_properties["bin_range"][0]
    histogram_properties["bin_range"] = (min_val, max_val)


def format_major_minor_ticks_log_scale(base: int, min_val: float, max_val: float):
    # Calculate the number of major ticks
    number_major_ticks = int(max_val - min_val + 1)

    # Calculate the number of minor ticks per major interval
    number_minor_ticks = int((max_val - min_val + 1) * 2)

    if number_major_ticks > 10:
        major_subs = np.arange(1, base, 2)
    else:
        major_subs = np.arange(1, base)

    if number_minor_ticks > 10:
        minor_subs = np.arange(1, base, 1)
    else:
        minor_subs = np.arange(1, base, 0.5)

    # Create the major and minor locators
    major_locator = ticker.LogLocator(base=base, subs=major_subs)
    minor_locator = ticker.LogLocator(base=base, subs=minor_subs)

    return major_locator, minor_locator


def plot_probabilities_lognormal_probit_with_best_fit(
    x_vals: list[float],
    color: Tuple[float, float, float],
    legend_label: str,
    axis: plt.Axes,
    legend_elements: list,
    x_label: str,
    y_label: str,
    show_markers: bool,
    best_fit_linestyle=output_file_constants.ProbitConstants.BEST_FIT_LINE_STYLE,
):
    x_values: np.ndarray = np.sort(x_vals)
    x_values = x_values[x_values > 0]
    y_values: np.ndarray = scipy.stats.mstats.plotting_positions(
        x_values,
        alpha=output_file_constants.ProbitConstants.PLOTTING_POSITION_ALPHA,
        beta=output_file_constants.ProbitConstants.PLOTTING_POSITION_BETA,
    )

    if show_markers:

        plt.scatter(
            x_values,
            y_values,
            color=color,
            label=legend_label,
            marker=output_file_constants.ProbitConstants.MARKER,
            facecolors="none",
            edgecolors=color,
            s=15,
        )

    axis.set_yscale(output_file_constants.ProbitConstants.Y_SCALE)
    axis.set_xscale(output_file_constants.ProbitConstants.X_SCALE)

    axis.xaxis.set_major_formatter(ticker.FuncFormatter(format_tick_labels_with_metric_prefix))
    major_locator, minor_locator = format_major_minor_ticks_log_scale(
        10, x_values.max(), x_values.min()
    )
    major_locator: ticker.LogLocator
    minor_locator: ticker.LogLocator
    axis.xaxis.set_major_locator(major_locator)
    axis.xaxis.set_minor_locator(minor_locator)
    axis.xaxis.set_minor_formatter(ticker.NullFormatter())
    axis.tick_params(
        axis="x", which="major", labelsize=output_file_constants.ProbitConstants.X_LABEL_SIZE
    )

    plt.xticks(rotation=45)

    best_fit_coefficients: np.ndarray = np.polyfit(
        np.log(x_values), scipy.stats.norm.ppf(y_values), 1
    )

    best_fit_line_y_intermediate: np.ndarray = (
        best_fit_coefficients[0] * np.log(x_values) + best_fit_coefficients[1]
    )

    best_fit_line_y_values: np.ndarray = scipy.stats.norm.cdf(best_fit_line_y_intermediate)

    plt.plot(
        x_values,
        best_fit_line_y_values,
        color=color,
        linestyle=best_fit_linestyle,
    )

    axis.set_xlabel(x_label)
    axis.set_ylabel(y_label)

    legend_elements.append(
        lines.Line2D(
            [0],
            [0],
            color=color,
            label=legend_label,
            markersize=15,
            linestyle=best_fit_linestyle,
        )
    )

    plt.tight_layout()
    plt.grid(True)
