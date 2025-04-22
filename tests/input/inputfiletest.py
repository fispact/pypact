import pypact as pp

from tests.testerbase import Tester


class InputFileTest(Tester):

    def test_reading_in_mass(self):
        ff = pp.InputData()
        pp.from_file(ff, 'reference/test.i')

        # Assert that the inventory is set to mass mode
        assert ff._inventoryismass is True, "Inventory should be set to mass mode"
        assert ff._inventoryisfuel is False, "Inventory should not be set to fuel mode"

        # Assert the total mass
        assert ff._inventorymass.totalMass == 1.0, "Total mass should be 1.0"

        # Assert the number of elements
        assert len(ff._inventorymass.entries) == 3, "There should be 3 elements in the inventory"

        # Assert the elements and their percentages
        expected_elements = [
            ("Ti", 80.0),
            ("Fe", 14.8),
            ("Cr", 5.2)
        ]
        for i, (element, percentage) in enumerate(expected_elements):
            assert ff._inventorymass.entries[i][0] == element, f"Element {i} should be {element}"
            assert ff._inventorymass.entries[i][1] == percentage, f"Percentage of {element} should be {percentage}"

    def test_reading_in_density(self):
        ff = pp.InputData()
        pp.from_file(ff, 'reference/test.i')

        assert ff._density == 19.5


    def test_reading_flux_and_time(self):
        ff = pp.InputData()
        pp.from_file(ff, 'reference/test.i')

        # Expected irradiation schedule (time in seconds, flux amplitude)
        expected_schedule = [
            (300.0, 1.1e15),
            (200.0, 42.0),
            (0.0, 0.0),
        ]

        # Assert the irradiation schedule matches the expected results
        assert len(ff._irradschedule) == len(expected_schedule), "Irradiation schedule length mismatch"
        for i, (time, flux) in enumerate(expected_schedule):
            assert ff._irradschedule[i][0] == time, f"Time mismatch at index {i}"
            assert ff._irradschedule[i][1] == flux, f"Flux mismatch at index {i}"