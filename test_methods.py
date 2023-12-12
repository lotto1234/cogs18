import pytest
from unittest import mock
from classes import House
from io import StringIO

def test_print_house_info():
    
    house = House("123 Test Street", -120.0, 35.0, 10, 5, 3, 4, 10)
    expected_output = (
        "House Attributes:\n"
        "Address: 123 Test Street\n"
        "Longitude: -120.0\n"
        "Latitude: 35.0\n"
        "House Age in years: 10\n"
        "Rooms: 5\n"
        "Bedrooms: 3\n"
        "Number of People: 4\n"
        "Monthly Income (in k USD): 10"
    )

    with mock.patch('sys.stdout', new=StringIO()) as fake_out:
        house.print_house_info()
        output = fake_out.getvalue().strip()
        assert output == expected_output

def test_print_all_addresses():
    
    House.instances = {
        "123 Test Street": mock.Mock(),
        "456 Sample Road": mock.Mock()
    }

    with mock.patch('sys.stdout', new=StringIO()) as fake_out:
        House.print_all_addresses()
        output = fake_out.getvalue().strip()
        assert "123 Test Street" in output
        assert "456 Sample Road" in output
        
def test_write_house_info_to_file():
    
    # Setup: Create a mock house instance
    house = House("123 Test Street", -120.0, 35.0, 10, 5, 3, 4, 10)

    expected_output = (
        "House Attributes:\n"
        "Address: 123 Test Street\n"
        "Longitude: -120.0\n"
        "Latitude: 35.0\n"
        "House Age: 10\n"
        "Rooms: 5\n"
        "Bedrooms: 3\n"
        "Number of People: 4\n"
        "Monthly Income (in k USD): 10\n"
        "House Price: 300000\n"
    )

    # Call the method to write the file
    house.write_house_info_to_file()

    # Read the content of the file
    file_path = f"{house.address.replace(' ', '_')}_info.txt"
    with open(file_path, "r") as file:
        content = file.read()

    # Assert that the file content is as expected
    assert content == expected_output


