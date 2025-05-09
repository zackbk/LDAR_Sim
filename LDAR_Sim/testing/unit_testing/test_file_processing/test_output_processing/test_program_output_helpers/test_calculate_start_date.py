"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        test_calculate_start_date.py
Purpose: Unit tests for the function to calculate the duration between dates,
specifically the function calculate_start_date
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

from file_processing.output_processing.program_output_helpers import calculate_start_date
import pandas as pd
from constants.output_file_constants import EMIS_DATA_COL_ACCESSORS as eca


def test_calculate_start_date():
    # Create a mock DataFrame for row
    sorted_by_site_summary = pd.DataFrame(
        {
            eca.PREV_CONDITION: [False, False, False, True, True],
            eca.SURVEY_COMPLETION_DATE: pd.date_range(start="1/1/2022", periods=5),
        }
    )

    # Test for proper start date generation
    expected_result = pd.Series(
        [
            pd.Timestamp("2022-01-01"),
            pd.Timestamp("2022-01-01"),
            pd.Timestamp("2022-01-02"),
            pd.Timestamp("2022-01-04"),
            pd.Timestamp("2022-01-05"),
        ]
    )
    actual_result = calculate_start_date(sorted_by_site_summary, 1)
    pd.testing.assert_series_equal(actual_result, expected_result)
