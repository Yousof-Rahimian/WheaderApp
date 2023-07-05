
# WheaderApp
The Weather App, developed by Yousof Rahimian in Python, uses OpenWeatherMap's API to retrieve weather information. It offers users real-time, high, and low temperatures, humidity levels, wind speed, wind direction, and a concise weather description for a chosen location. Users can input either city names or US zip codes. Additionally, temperature units can be customized to Celsius, Fahrenheit, or Kelvin.





## Features
-  Accepts city name or US zip code as input.
-  Users can choose their preferred temperature unit: Celsius, Fahrenheit, or Kelvin.
-  Provides comprehensive weather data: current, high, and low temperatures, feels-like temperature, humidity level, wind speed, and wind direction.
-  Translates wind direction degrees into cardinal directions.
-  Prompts for another query after each search, allowing for continuous use.
-  Error handling to ensure correct input values and to handle exceptions during data fetching.
## Code Structure



The project consists of a single Python file with the following key components:

- WeatherData: A class that encapsulates weather information. It includes a print function that dynamically adjusts the displayed data based on the chosen temperature unit.
- fetch_data: A function that fetches weather data from the OpenWeatherMap API. It accepts a city name, US zip code, and temperature unit type as inputs and returns an instance of WeatherData with the fetched data.
- wind_direction: A function that translates wind direction from degrees to cardinal directions.
- main: The main function that drives the program. It handles user inputs and calls other functions based on these inputs.
## Prerequisites
- Python 3.6 or later.
- The requests library for sending HTTP requests.
- A free API key from OpenWeatherMap. Replace the placeholder in the fetch_data function with your actual API key.


## How to Use
To use the application, simply run the Python script in your terminal or command prompt. The application will guide you through the rest with its prompts.

- The program will first ask you to choose between providing a city name or a US zip code.
- After choosing the type of location identifier, you will be asked to input the city name or zip code.
- Then you will be asked to choose the preferred temperature unit.
- The program will fetch and display the weather data for the specified location.
- Finally, you will be asked if you want to perform another search. If you choose to do so, the program will start over from step 1.
Please feel free to contribute to the development of this project by submitting pull requests.e

