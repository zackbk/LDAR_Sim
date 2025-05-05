from datetime import date
from typing import Tuple
from src.virtual_world.sites import Site
from src.file_processing.input_processing.emissions_source_processing import EmissionsSourceSample
from testing.unit_testing.test_virtual_world.test_sites.sites_testing_fixtures import (  # noqa
    mock_site_for_simple_generate_emissions_fix,
)


def test_000_generate_emissions_properly_generates_emissions_for_simple_site(
    mock_site_for_simple_generate_emissions: Tuple[Site, date, date]
):
    site: Site = mock_site_for_simple_generate_emissions[0]
    start_date: date = mock_site_for_simple_generate_emissions[1]
    end_date: date = mock_site_for_simple_generate_emissions[2]
    emissions: dict = site.generate_emissions(
        start_date,
        end_date,
        1,
        emission_rate_source_dictionary={
            "test": EmissionsSourceSample("test", "gram", "second", [1], 1000)
        },
        repair_delay_dataframe={},
        pre_simulation_emissions=True,
    )
    assert emissions is not None
