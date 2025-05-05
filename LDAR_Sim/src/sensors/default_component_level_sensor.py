"""
------------------------------------------------------------------------------
Program:     The LDAR Simulator (LDAR-Sim)
File:        default_component_level_sensor.py
Purpose: The provides default behaviors for component level sensors

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

from typing import Union
from constants.sensor_constants import QuantificationTypes
from scheduling.schedule_dataclasses import (
    EmissionDetectionReport,
    EquipmentGroupSurveyReport,
    SiteSurveyReport,
)
from sensors.default_sensor import DefaultSensor
from virtual_world.emission_types.emission import Emission
from virtual_world.sites import Site
from constants.param_default_const import Levels


class DefaultComponentLevelSensor(DefaultSensor):
    SURVEY_LEVEL = Levels.COMPONENT_LEVEL

    def __init__(
        self,
        mdl: Union[list[float], float],
        quantification_parameters: list[float],
        quantification_type: str = QuantificationTypes.DEFAULT.value,
        input_dir: str = None,
    ) -> None:
        super().__init__(
            mdl,
            quantification_parameters,
            quantification_type,
            input_dir=input_dir,
        )

    def detect_emissions(self, site: Site, meth_name: str, survey_report: SiteSurveyReport) -> bool:
        # TODO update and test this functionality
        detectable_emissions: dict[str, dict[str, list[Emission]]] = site.get_detectable_emissions(
            method_name=meth_name
        )
        eqg_survey_reports: list[EquipmentGroupSurveyReport] = []
        site_level_emission_rate: float = 0.0
        site_level_measured_rate: float = 0.0

        for eqg, eq_emis_list in detectable_emissions.items():
            eqg_level_emis_rate: float = 0.0
            eqg_level_measured_rate: float = 0.0
            emissions_detection_reports: list[EmissionDetectionReport] = []

            for comp, emis_list in eq_emis_list.items():
                equip_rate: float = sum([emission.get_rate() for emission in emis_list])

                equip_emission_detected: bool = self._rate_detected(equip_rate)

                if equip_emission_detected:
                    equip_measured_rate: float = self._measure_rate(equip_rate)
                else:
                    equip_measured_rate: float = 0

                emissions_detection_reports.append(
                    self._gen_emissions_detection_report(
                        site.get_id(), eqg, comp, equip_measured_rate, equip_rate
                    )
                )

                eqg_level_emis_rate += equip_rate
                eqg_level_measured_rate += equip_measured_rate

            eqg_survey_reports.append(
                self._gen_eqg_survey_report(
                    site_id=site.get_id(),
                    eqg_id=eqg,
                    true_rate=eqg_level_emis_rate,
                    measured_rate=eqg_level_measured_rate,
                    emissions_detection_reports=emissions_detection_reports,
                )
            )

            site_level_emission_rate += eqg_level_emis_rate
            site_level_measured_rate += eqg_level_measured_rate

        self._fill_detection_report(
            survey_report, site_level_emission_rate, site_level_measured_rate, eqg_survey_reports
        )

        return site_level_measured_rate != 0

    def _fill_detection_report(
        self,
        survey_report: SiteSurveyReport,
        true_site_rate: float,
        measured_site_rate: float,
        eqg_survey_reports: list[EquipmentGroupSurveyReport],
    ) -> None:
        survey_report.site_true_rate = true_site_rate
        survey_report.site_measured_rate = measured_site_rate
        survey_report.survey_level = self.SURVEY_LEVEL
        survey_report.equipment_groups_surveyed = eqg_survey_reports

    def _gen_eqg_survey_report(
        self,
        site_id: str,
        eqg_id: str,
        true_rate: float,
        measured_rate: float,
        emissions_detection_reports: list[EmissionDetectionReport],
    ) -> EquipmentGroupSurveyReport:
        eqg_survey_report: EquipmentGroupSurveyReport = EquipmentGroupSurveyReport(
            site_id,
            eqg_id,
            measured_rate=measured_rate,
            true_rate=true_rate,
            emissions_detected=emissions_detection_reports,
        )
        return eqg_survey_report

    def _gen_emissions_detection_report(
        self, site_id: str, eqg_id: str, comp_id: str, measured_rate: float, true_rate: float
    ) -> EmissionDetectionReport:
        emis_detect_report = EmissionDetectionReport(
            site=site_id,
            equipment_group=eqg_id,
            component=comp_id,
            measured_rate=measured_rate,
            true_rate=true_rate,
        )
        return emis_detect_report
