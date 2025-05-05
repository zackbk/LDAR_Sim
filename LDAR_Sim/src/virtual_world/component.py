"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        component.py
Purpose: The component module.

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

from copy import deepcopy
from datetime import date
import logging
import re
from typing import Any
import sys
import pandas as pd
from file_processing.output_processing.output_utils import (
    EmisInfo,
    TsEmisData,
)
from file_processing.input_processing.emissions_source_processing import (
    EmissionsSource,
)
from scheduling.schedule_dataclasses import TaggingInfo
from constants.output_file_constants import EMIS_DATA_COL_ACCESSORS as eca
from virtual_world.emission_types.emission import Emission
from virtual_world.emission_types.repairable_emission import RepairableEmission
from virtual_world.emission_types.non_repairable_emissions import NonRepairableEmission
from constants.infrastructure_const import Infrastructure_Constants as IC
from constants.error_messages import Initialization_Messages as im
from virtual_world.sources import Source


class Component:
    def __init__(self, equip_type, equip_id, infrastructure_inputs, prop_params) -> None:
        STR_FILTER = r"_equipment"
        pattern: re.Pattern[str] = re.compile(re.escape(STR_FILTER), re.IGNORECASE)
        self._equip_type: str = re.sub(pattern, "", equip_type)
        self._component_ID: str = self._equip_type + "_" + str(equip_id)
        self._sources: list[Source] = []
        self._create_sources(infrastructure_inputs=infrastructure_inputs, prop_params=prop_params)
        self._active_emissions: list[Emission] = []
        self._inactive_emissions: list[Emission] = []
        self.emis_sum_dtypes: dict[str, str] = {}

    def __reduce__(self):
        args = (
            self._equip_type,
            self._component_ID,
            self._sources,
            self._active_emissions,
            self._inactive_emissions,
            self.emis_sum_dtypes,
        )
        return (self.__class__._reconstruct, args)

    @classmethod
    def _reconstruct(
        cls,
        equip_type,
        component_ID,
        sources,
        active_emissions,
        inactive_emissions,
        emis_sum_dtypes,
    ):
        instance = cls.__new__(cls)
        instance._equip_type = equip_type
        instance._component_ID = component_ID
        instance._sources = sources
        instance._active_emissions = active_emissions
        instance._inactive_emissions = inactive_emissions
        instance.emis_sum_dtypes = emis_sum_dtypes
        return instance

    def set_emis_sum_dtypes(self, methods: list[str]):
        self.emis_sum_dtypes = Emission.EMIS_SUMMARY_DTYPES
        method_spat_dtypes = {method: "bool" for method in methods}
        self.emis_sum_dtypes.update(method_spat_dtypes)

    # def _get_methods_for_dtype(self, prop_params) -> dict[str, str]:
    #     # Loop through any method specific param to get the existing methods

    #     method_spat_dtypes = {}
    #     for method in next(iter(prop_params["Method_Specific_Params"].values())):
    #         method_spat_dtypes[f"{method} Spatial Coverage"] = "bool"

    #     return method_spat_dtypes

    def _create_sources(self, infrastructure_inputs, prop_params) -> None:
        if self._equip_type != "Placeholder" and "sources" in infrastructure_inputs:
            sources_info: pd.DataFrame = infrastructure_inputs["sources"]
            sources: pd.DataFrame = sources_info.loc[
                sources_info[IC.Sources_File_Constants.COMPONENT] == self._equip_type
            ]
            for idx, source in sources.iterrows():
                src_prop_params = deepcopy(prop_params)
                src_id = source[IC.Sources_File_Constants.SOURCE]
                self._sources.append(Source(src_id, source, src_prop_params))
        elif self._equip_type == "Placeholder":
            src_id = "Placeholder_Rep"
            placeholder_source_info = {
                IC.Sources_File_Constants.REPAIRABLE: True,
                IC.Sources_File_Constants.PERSISTENT: True,
                IC.Sources_File_Constants.ACTIVE_DUR: 1,
                IC.Sources_File_Constants.INACTIVE_DUR: 0,
            }
            self._sources.append(Source(src_id, placeholder_source_info, prop_params))
            src_id_nonrep = "Placeholder_NonRep"
            placeholder_nonrep_source_info = {
                IC.Sources_File_Constants.REPAIRABLE: False,
                IC.Sources_File_Constants.PERSISTENT: True,
                IC.Sources_File_Constants.ACTIVE_DUR: 1,
                IC.Sources_File_Constants.INACTIVE_DUR: 0,
            }
            self._sources.append(Source(src_id_nonrep, placeholder_nonrep_source_info, prop_params))
        elif self._equip_type == "Placeholder_Rep":
            src_id = "Placeholder_Rep"
            placeholder_source_info = {
                IC.Sources_File_Constants.REPAIRABLE: True,
                IC.Sources_File_Constants.PERSISTENT: True,
                IC.Sources_File_Constants.ACTIVE_DUR: 1,
                IC.Sources_File_Constants.INACTIVE_DUR: 0,
            }
            self._sources.append(Source(src_id, placeholder_source_info, prop_params))
        elif self._equip_type == "Placeholder_NonRep":
            src_id_nonrep = "Placeholder_NonRep"
            placeholder_nonrep_source_info = {
                IC.Sources_File_Constants.REPAIRABLE: False,
                IC.Sources_File_Constants.PERSISTENT: True,
                IC.Sources_File_Constants.ACTIVE_DUR: 1,
                IC.Sources_File_Constants.INACTIVE_DUR: 0,
            }
            self._sources.append(Source(src_id_nonrep, placeholder_nonrep_source_info, prop_params))
        else:
            logger: logging.Logger = logging.getLogger(__name__)
            logger.error(im.SOURCE_CREATION_ERROR_MESSAGE)
            sys.exit()

    def generate_emissions(
        self,
        sim_start_date,
        sim_end_date,
        sim_number,
        emission_rate_source_dictionary: dict[str, EmissionsSource],
        repair_delay_dataframe: pd.DataFrame,
        pre_simulation_emissions: bool,
    ) -> dict:
        equip_emissions = {}
        for src in self._sources:
            equip_emissions.update(
                src.generate_emissions(
                    sim_start_date,
                    sim_end_date,
                    sim_number,
                    emission_rate_source_dictionary,
                    repair_delay_dataframe,
                    pre_simulation_emissions=pre_simulation_emissions,
                )
            )

        return {self._component_ID: equip_emissions}

    def activate_emissions(self, date: date, sim_number: int) -> int:
        """Activate any emissions that are due to begin on the current date for the given simulation
        and add them to the active emissions list for the component at which they occur.

        Args:
            date (date): The current date in simulation.
            sim_number (int): The simulation number.
            Used to interact with the correct set of emissions.
        """
        new_emissions_count: int = 0
        new_emissions_list: list[Emission] = []
        for source in self._sources:
            new_emissions: list[Emission] = source.activate_emissions(date, sim_number)
            new_emissions_list.extend(new_emissions)

        new_emissions_count += len(new_emissions_list)
        self._active_emissions.extend(new_emissions_list)
        return new_emissions_count

    def update_emissions_state(self, emis_rep_info: EmisInfo, emis_data: TsEmisData) -> None:
        updated_active_emissions: list[Emission] = []
        for emission in self._active_emissions:
            if emission.update(emis_rep_info):
                updated_active_emissions.append(emission)
                emis_total_daily = emission.get_daily_emis()
                if emission._repairable:
                    emis_data.daily_emis_mit += emis_total_daily
                else:
                    emis_data.daily_emis_non_mit += emis_total_daily
                emis_data.daily_emis += emis_total_daily
            else:
                self._inactive_emissions.append(emission)
        self._active_emissions = updated_active_emissions
        emis_data.active_leaks += len(self._active_emissions)

    def tag_emissions(self, tagging_info: TaggingInfo) -> None:
        # TODO improve this logic
        emission_rate = tagging_info.measured_rate / len(self._active_emissions)
        for emission in self._active_emissions:
            if isinstance(emission, RepairableEmission):
                emission.tag_leak(
                    measured_rate=emission_rate,
                    cur_date=tagging_info.curr_date,
                    t_since_ldar=tagging_info.t_since_LDAR,
                    company=tagging_info.company,
                    crew_id=tagging_info.crew,
                    tagging_rep_delay=tagging_info.report_delay,
                )
                emission.update_detection_records(
                    company=tagging_info.company, detect_date=tagging_info.curr_date
                )
            elif isinstance(emission, NonRepairableEmission):
                emission.record_emission(
                    measured_rate=emission_rate,
                    cur_date=tagging_info.curr_date,
                    t_since_ldar=tagging_info.t_since_LDAR,
                    company=tagging_info.company,
                    crew_id=tagging_info.crew,
                )
                emission.update_detection_records(
                    company=tagging_info.company, detect_date=tagging_info.curr_date
                )

    def get_detectable_emissions(self, method_name: str) -> Emission:
        detectable_emissions: list[Emission] = []
        for emis in self._active_emissions:
            if emis.check_spatial_cov(method_name) and emis.is_emitting():
                if emis.check_temporal_cov(method_name):
                    detectable_emissions.append(emis)

        return detectable_emissions

    def set_pregen_emissions(self, equipment_emissions, sim_number) -> None:
        for src in self._sources:
            src.set_pregen_emissions(equipment_emissions[src.get_id()], sim_number)

    def get_id(self) -> str:
        return self._component_ID

    def gen_emis_data(
        self, emis_df: pd.DataFrame, site_id: str, eqg_id: str, row_index: int, end_date: date
    ) -> int:
        upd_row_index = row_index
        for emission in self._active_emissions:
            summary_dict: dict[str, Any] = emission.get_summary_dict(end_date)
            summary_dict.update(
                {eca.SITE_ID: site_id, eca.EQG: eqg_id, eca.COMP: self._component_ID}
            )
            emis_df.loc[upd_row_index] = summary_dict
            upd_row_index += 1

        for emission in self._inactive_emissions:
            summary_dict: dict[str, Any] = emission.get_summary_dict(end_date)
            summary_dict.update(
                {eca.SITE_ID: site_id, eca.EQG: eqg_id, eca.COMP: self._component_ID}
            )
            emis_df.loc[upd_row_index] = summary_dict
            upd_row_index += 1
        return upd_row_index
