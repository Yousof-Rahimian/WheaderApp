
# DSC510
# Final Project
# Programming Assignment - Final Project
# Author: Yousof Rahimian
# 8/14/2021
# Description: This program will prompt the user for their city/zip code and request
# forecast data from the OpenWeatherMap API


# imported libraries
import json
import pandas as pd
import requests
from time import time, ctime
from prettytable import PrettyTable
from textwrap import wrap
import re


# One function for retrieving the city list bulk file from Open Weather Map
# This function uses the pandas function, read_json, to convert the JSON output from the url into a pandas object
# Creation of a pandas dataframe to utilize
def getCityList():
    url = 'http://bulk.openweathermap.org/sample/city.list.json.gz'
    df = pd.read_json(url)
    return df


# Function for validating the user-inputted zipcode
# re.match will return True if the zip_code entered follows the regex rules
# \b - Defines a word boundary start
# \d - "digits" or numbers
# {5} - matches 5 times
# \b - Close your word boundary
def validate_zip(zip_code):
    return re.match(r'\b\d{5}\b', zip_code)


# Function for generating the API call for when the user enters a city name
# Uses requests library functions
# Also handles exceptions for when the request to the API is not successful (200)
# Prints the JSON contents for that certain city from the API
def getAPICity(cityName, APIKey):
    # Assembling API call with city name from user
    call = "http://api.openweathermap.org/data/2.5/weather?q=" + cityName + ",us&appid=" + APIKey + "&units=imperial"
    responseCity = requests.get(call)
    try:
        responseCity.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("Error: " + str(e))
    return responseCity.json()


# Function for generating the API call for when the user enters a zipcode
# Uses requests library functions
# Also handles exceptions for when the request to the API is not successful (200)
# Prints the JSON contents for that certain zipcode from the API
def getAPIZip(zipCode, APIKey):
    call = "http://api.openweathermap.org/data/2.5/weather?zip=" + zipCode + ",us&appid=" + APIKey + "&units=imperial"
    responseZip = requests.get(call)
    try:
        responseZip.raise_for_status()
    except requests.exceptions.HTTPError as e:
        # Status code was not a 200 -- means successful
        print("Error: " + str(e))
    # Status code was 200
    return responseZip.json()


# Function for generating the API call for when the user enters a city name and a state abbreviation
# Program handles if the city exists in multiple states
# Prints the JSON contents for that certain city from the API
def getAPICityState(cityName, stateCode, APIKey):
    # Assembling API call with city name from user
    APIInput = cityName + "," + stateCode
    call = 'https://api.openweathermap.org/data/2.5/weather?q={},us&' \
           'appid={}&units=imperial'.format(APIInput, APIKey)
    responseCity = requests.get(call)
    try:
        responseCity.raise_for_status()
    except requests.exceptions.HTTPError as e:
        print("Error: " + str(e))
    return responseCity.json()



# This function utilizes the cities dataframe created from the getCityList() function
# To retrieve the possible state codes affiliated with the city entered by the user
def cityLookup(city):
    # Dataframe with the city list from the OpenWeatherMap bulk file
    df = getCityList()
    # State codes that exist for the particular city
    statesCity = df.loc[(df["name"] == city) & (df['country'] == 'US'), ["state"]].values.tolist()
    # Number of state codes affiliated with the city name entered by the user
    count_state = len(statesCity)

    # Creation of a dictionary to hold the values retrieved from the dataframe for the given city
    states_dict = {}
    # Adding count and list of state abbreviations to states_dict
    states_dict['City'] = city
    states_dict['State_Count'] = count_state
    states_dict['State_Name'] = statesCity
    return states_dict


# Must install pandas and use --> import pandas as pd
# The API will allow an improper combo to be entered and still output information for the city
# So I wanted to handle if this non-existent combo is given
def validate_city_state(city_name, state_code):
    # Get the city list from OpenWeatherMap, read to pandas dataframe
    df = getCityList()

    # Search dataframe for city_name, state_code combination
    # df['country'] == 'US' - ONLY US CITIES IN SCOPE FOR FINAL PROJECT
    location_query = df.loc[(df['name'] == city_name) & (df['state'] == state_code) & (df['country'] == 'US'),
                            ['id', 'name', 'state', 'country', 'coord']]
    # If only one exists, set city name and state_code or any combo of them
    if len(location_query) == 1:
        # Get values from pandas series of results
        city = str(location_query['name'].iloc[0]).strip()
        state_code = str(location_query['state'].iloc[0]).strip()
        city_state = (city + ', ' + state_code)

    return city, state_code




# jprint function
# Prints the JSON output from the API call in a formatted string
# Uses the json.dumps() main function
def jprintDict(obj):
    # json.dumps turns Python object into a JSON string
    text = json.dumps(obj, sort_keys=True, indent=4)
    # json.loads converts a JSON string into a Python dictionary
    resp = json.loads(text)
    # Getting essential attributes from resp dictionary
    # Also error handling for if invalid city or zip code is given
    outputDict = {}
    try:
        outputDict["Name"] = resp["name"]
        outputDict["Country"] = resp["sys"]["country"]
        outputDict["Current Weather"] = resp["weather"][0]["description"].title()
        outputDict["Current Temperature"] = str(resp["main"]["temp"]) + "°"
        outputDict["High"] = str(resp["main"]["temp_max"]) + "°"
        outputDict["Low"] = str(resp["main"]["temp_min"]) + "°"
        outputDict["Sunrise"] = ctime(resp["sys"]["sunrise"])
        outputDict["Sunset"] = ctime(resp["sys"]["sunset"])
        outputDict["Humidity"] = str(resp["main"]["humidity"]) + "%"
        outputDict["Wind Speed"] = str(resp["wind"]["speed"]) + " mph"
        outputDict["Feels like"] = str(resp["main"]["feels_like"]) + "°"
        outputDict["Pressure"] = str(resp["main"]["pressure"]) + " hPa"
        outputDict["Visibility"] = str(resp["visibility"]) + " m"

        # Pretty print in tabular format
        tab = PrettyTable(['label', 'value'])
        for key, val in outputDict.items():
            wrapped_value_lines = wrap(str(val)) or ['']
            tab.add_row([key, wrapped_value_lines[0]])
            for subseq in wrapped_value_lines[1:]:
                tab.add_row(['', subseq])
        print(tab)
    except:
        print("That city can't be found!")
        print()


# Main method for prompting the user for a zip code/city to get forecast data from
def main():
    apiKey = input("\nEnter your API Key for this session! ")
    # Two while loops -- one for continuing to get weather and another one for handling zip/state/q input
    # while loops for continuing to get weather
    while True:
        zipCity = input("\n Possible values: {'Zip', 'City', 'Q to quit'}, which one do you like? ")
        zipCity = zipCity.strip().lower()
        while True:
            # If/else statements for zipcode input
            # Must be exactly 5 characters
            if zipCity == 'zip':
                zipCode = input("\nPlease enter the zip code you want the forecast for: ").strip().lower()
                allowedZip = validate_zip(zipCode)
                if allowedZip:
                    jprintDict(getAPIZip(zipCode, apiKey))
                    break
                else:
                    print("That zip code is not valid. Please try again. Must be exactly 5 digits! ")
                    continue
            # If/else statements for city name input
            elif zipCity == 'city':
                cityName = input("\nPlease enter the city you want the forecast for: ").strip().title()
                # Retrieving the state information for the city entered
                lookup_dict = cityLookup(cityName)
                # This city exists in more than one US state
                if lookup_dict['State_Count'] > 1:
                    while True:
                        print("\nThe city you entered exists in " + str(lookup_dict['State_Count']) + " states: ")
                        print(', '.join(' '.join(map(str, state)) for state in lookup_dict['State_Name']))
                        stateAbbrev = input(
                            "Which state is your city located in? Enter the state abbreviation: ").strip().upper()
                        # validating the city name and state code entered by the user
                        # try/except for error handling if improper combo is given
                        try:
                            city, state_code = validate_city_state(cityName, stateAbbrev)
                        except:
                            print("That city & state combo does not exist! Please enter one from the list given.\n")
                            continue
                        else:
                            print("\n+------------Weather in " + city + "," + state_code + "---------+")
                            jprintDict(getAPICityState(city, state_code, apiKey))
                            break
                    # jprintDict(getAPICityState(cityName,stateAbbrev,apiKey))

                # This city only exists in one US state
                elif lookup_dict['State_Count'] == 1:
                    # Retrieving the independent state value from the list of lists in the dictionary
                    state_code = lookup_dict['State_Name'][0][0]
                    print(cityName + " only exists in one state in the US!")
                    print("\n+----------------Weather in " + cityName + "," + str(state_code) + "---------------+")
                    # Testing API call
                    jprintDict(getAPICity(cityName, apiKey))
                # City was not found in lookup -- error handling
                else:
                    print("That city was not found!")
                break
            # If/else statement for quitting the program if user wants
            elif zipCity == 'q':
                print("Hope you enjoyed checking the weather! Have a great day!")
                exit()
            # Handling if proper input value is not given
            else:
                print("That value is not valid.")
                break


if __name__ == "__main__":
    main()

