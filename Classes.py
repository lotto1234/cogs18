from sklearn.linear_model import LinearRegression
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

class House:
    """
    A class to represent a house with various attributes and capabilities for price prediction.

    Attributes:
    address (str): The address of the house.
    longitude (float): The longitude coordinate of the house.
    latitude (float): The latitude coordinate of the house.
    house_age (float): The age of the house in years.
    rooms (float): Number of rooms in the house.
    bedrooms (float): Number of bedrooms in the house.
    number_of_people (float): Number of people living in the house.
    monthly_income_in_k_USD (float): Monthly income of the household in thousand USD.
    house_price (float): Predicted price of the house (default is None).

    Class Attributes:
    instances (dict): A dictionary to store instances of the House class.
    """

    instances = {}

    def __init__(self, address, longitude, latitude, house_age, rooms, bedrooms, number_of_people, monthly_income_in_k_USD):
        """
        Constructs all the necessary attributes for the House object.

        Parameters:
        address (str): Address of the house.
        longitude (float): Longitude of the house.
        latitude (float): Latitude of the house.
        house_age (float): Age of the house in years.
        rooms (float): Number of rooms in the house.
        bedrooms (float): Number of bedrooms in the house.
        number_of_people (float): Number of people living in the house.
        monthly_income_in_k_USD (float): Monthly income of the household in thousand USD.
        """
        self.address = address
        self.longitude = longitude
        self.latitude = latitude
        self.house_age = house_age
        self.rooms = rooms
        self.bedrooms = bedrooms
        self.number_of_people = number_of_people
        self.monthly_income_in_k_USD = monthly_income_in_k_USD
        self.house_price = None
        
        # Adding the new instance to the class-wide instance dictionary
        House.instances[address] = self

    def predict_house_price(self):
        """
        Predicts the house price using linear regression model and plots its comparison with other house prices.
        """
        # Loading the dataset
        df = pd.read_csv('final_data.csv')
        # Removing any unnamed columns that may be present
        df = df.drop([col for col in df.columns if "unnamed" in col.lower()], axis=1)
        
        # Creating and training the linear regression model
        linear_model = LinearRegression()
        linear_model.fit(df.drop('house_value', axis=1), df['house_value'])

        # Preparing data for prediction
        new_entry = {
            'longitude': self.longitude,
            'latitude': self.latitude,
            'house_age': self.house_age,
            'rooms': self.rooms,
            'bedrooms': self.bedrooms,
            'number_of_people': self.number_of_people,
            'monthly_income_in_k_USD': self.monthly_income_in_k_USD
        }
        new_entry_df = pd.DataFrame([new_entry])

        # Predicting the house value
        predicted_value = linear_model.predict(new_entry_df)
        self.house_price = predicted_value[0]

        # Plotting the prediction in context with the dataset
        plt.figure(figsize=(10, 6))
        plt.hist(df['house_value'], bins=30, alpha=0.7, color='blue')
        plt.axvline(predicted_value, color='red', linestyle='dashed', linewidth=2)
        plt.title('Your house value compared to others')
        plt.xlabel('House Value')
        plt.ylabel('Frequency')
        plt.legend(['Your House Price', 'House Value'])
        plt.show()

    @staticmethod
    def print_all_addresses():
        """
        Prints the addresses of all houses stored in the class instance dictionary.
        """
        print("Addresses of all houses:")
        for address in House.instances:
            print(address)
    
    def print_house_info(self):
        """
        Prints the detailed information of the house instance.
        """
        print("House Attributes:")
        print(f"Address: {self.address}")
        print(f"Longitude: {self.longitude}")
        print(f"Latitude: {self.latitude}")
        print(f"House Age in years: {self.house_age}")
        print(f"Rooms: {self.rooms}")
        print(f"Bedrooms: {self.bedrooms}")
        print(f"Number of People: {self.number_of_people}")
        print(f"Monthly Income (in k USD): {self.monthly_income_in_k_USD}")
        if self.house_price is not None:
            print(f"House Price: {self.house_price}")

    def write_house_info_to_file(self):
        """
        Writes the house's attributes to a text file named after the house's address.
        """
        with open(f"{self.address.replace(' ', '_')}_info.txt", "w") as file:
            file.write("House Attributes:\n")
            file.write(f"Address: {self.address}\n")
            file.write(f"Longitude: {self.longitude}\n")
            file.write(f"Latitude: {self.latitude}\n")
            file.write(f"House Age: {self.house_age}\n")
            file.write(f"Rooms: {self.rooms}\n")
            file.write(f"Bedrooms: {self.bedrooms}\n")
            file.write(f"Number of People: {self.number_of_people}\n")
            file.write(f"Monthly Income (in k USD): {self.monthly_income_in_k_USD}\n")
            if self.house_price is not None:
                file.write(f"House Price: {self.house_price}\n")