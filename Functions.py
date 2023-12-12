from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsRegressor
import pandas as pd
import numpy as np
from IPython.display import Image, display
from classes import House


def impute_knn(df):
    
    ''' inputs: pandas df containing feature matrix
    
    !NOT MY CODE! SOURCE:
    https://www.kaggle.com/code/shtrausslearning/bayesian-regression-house-price-prediction/notebook
    
    outputs: dataframe with NaN imputed '''
    ldf = df.select_dtypes(include=[np.number])           # select numerical columns in df
    ldf_putaside = df.select_dtypes(exclude=[np.number])  # select categorical columns in df
    # define columns w/ and w/o missing data
    cols_nan = ldf.columns[ldf.isna().any()].tolist()         # columns w/ nan 
    cols_no_nan = ldf.columns.difference(cols_nan).values     

    for col in cols_nan:                
        imp_test = ldf[ldf[col].isna()]   # indicies which have missing data will become our test set
        imp_train = ldf.dropna()          # all indicies which which have no missing data 
        model = KNeighborsRegressor(n_neighbors=5)  # KNR Unsupervised Approach
        knr = model.fit(imp_train[cols_no_nan], imp_train[col])
        ldf.loc[df[col].isna(), col] = knr.predict(imp_test[cols_no_nan])
    
    return pd.concat([ldf,ldf_putaside],axis=1)

def house_wrapper():
    """
    Wrapper function to handle house management operations.

    This function provides a menu for the user to choose from various house management options.
    It maps user inputs to the coresponding functions.
    """
    options = """
    Hi there, you have the following options:
    1. Add a new house to your list
    2. Delete a house from your list
    3. Print the information for a house
    4. Estimate the price of a house
    5. Return a list of all houses
    6. Quit the program
    You can always type in "BACK" to go back to this menu.
    """

    function_mapping = {
        1: add_new_house,
        2: delete_house,
        3: print_house_info,
        4: estimate_price,
        5: list_all_houses,
        6: quit_function
    }

    print(options)
    try:
        user_choice = int(go_back(input("Enter a number between 1 and 6: ")))
        if 1 <= user_choice <= 6:
            function_mapping[user_choice]()
        else:
            print("Please enter a valid number between 1 and 6.")
            house_wrapper()
    except ValueError:
        print("Invalid input! Please enter a number.")
        house_wrapper()

def print_house_info():
    """
    Print information for a specific house.

    The user is prompted to choose between printing information here or to a text file.
    He is then asked to enter the address of the house.
    """
    user_input = go_back(input("Do you want the information to be printed in here or printed to a text file? Write HERE or TEXT: "))
    
    if user_input.upper() == "HERE":
        address = go_back(input("Enter the address of the house: "))
        house = House.instances.get(address)
        if house:
            house.print_house_info()
        else:
            print("House not found for this address.")
    elif user_input.upper() == "TEXT":
        address = go_back(input("Enter the address of the house: "))
        house = House.instances.get(address)
        if house:
            house.write_house_info_to_file()
            print("A file with the data has been created in this directory.")
        else:
            print("House not found for this address.")
    else:
        print("Invalid input.")
    house_wrapper()

def delete_house():
    """
    Deletes a house from the list based on the address provided by the user.
    """
    address = go_back(input("Enter the address of the house to delete: "))
    if address in House.instances:
        del House.instances[address]
        print(f"House at {address} has been deleted.")
    else:
        print("House not found.")
    house_wrapper()

def estimate_price():
    """
    Estimates the price of a house based on its attributes using Sklearn and refers to a method in the House class.

    The user is asked to enter the address of the house for which the price prediction is required so that the method can be executed on the corresponding object.
    """
    address = go_back(input("Enter the address of the house: "))
    house = House.instances.get(address)
    if house:
        house.predict_house_price()
    else:
        print("House not found for this address.")
    house_wrapper()

def list_all_houses():
    """
    Prints the addresses of all houses in the list using the dictionary defined in the class.
    """
    House.print_all_addresses()
    house_wrapper()

def add_new_house():
    """
    Creates a new object of the house class and it appends it to the dict of houses with their addresses.

    The user is prompted to enter various attributes of the house such as address, longitude, latitude, etc.
    """
    print("Great, let's start!\nI am now going to ask you some basic questions about your house: ")
    address = go_back(input("Enter the address of the house: "))
    #shows a map of california with longitude and latitude so that you know what numbers to put in
    display(Image(filename='California_Map.png', width=450, height=450))
    longitude = float(go_back(input("Enter the longitude of the house: ")))
    latitude = float(go_back(input("Enter the latitude of the house: ")))
    house_age = float(go_back(input("Enter the age of the house: ")))  
    rooms = float(go_back(input("Enter the number of rooms: ")))  
    bedrooms = float(go_back(input("Enter the number of bedrooms: ")))  
    number_of_people = float(go_back(input("Enter the number of people who live in the house: ")))  
    monthly_income_in_k_USD = float(go_back(input("Enter the monthly household income in k USD: ")))  

    new_house = House(address, longitude, latitude, house_age, 
                      rooms, bedrooms, 
                      number_of_people, monthly_income_in_k_USD)
    
    print("Great, now we have created a new house!\n")
    house_wrapper()

def quit_function():
    """
    Quits the program by leaving the cycle of repeatedly calling the wrapper function.
    """
    print("You have quit the program.")
    
def go_back(entry):
    """
    Allows you to go to the wrapper
    """
    if entry == "BACK":
        house_wrapper()
    else:
        return entry
