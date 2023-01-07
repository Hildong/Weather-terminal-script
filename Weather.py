import requests
from geopy.geocoders import Nominatim 
from datetime import datetime
print(datetime.date(datetime.now())) ##For Date
exitProgram = False

# Get longitude and latitude of requested city
def getLongAndLat():
    # Init Nominatim API
    geolocator = Nominatim(user_agent="TerminalWeatherApi")
    city = input("Please provide the city of temperature you want: ")

    return geolocator.geocode(city)

# Get todays forcast
def todaysForcast():
    url = "https://archive-api.open-meteo.com/v1/archive?latitude=" + str(getLongAndLat().latitude) + "&longitude=" + str(getLongAndLat().longitude) + "&start_date=" + datetime.date(datetime.now()) + "&" + datetime.date(datetime.now()) + "&hourly=temperature_2m"
    response = requests.request("GET", url)

    print(response.text)

# Get forcast for x amount of days forward
def futureForcast():
    url = "https://archive-api.open-meteo.com/v1/archive?latitude=" + str(getLongAndLat().latitude) + "&longitude=" + str(getLongAndLat().longitude) + "&start_date=2023-01-08&end_date=2023-01-15&hourly=temperature_2m"


    response = requests.request("GET", url)

    print(response.text)

# Get average temperature of todays date x years back
def todaysAverage():
    url = "https://archive-api.open-meteo.com/v1/archive?latitude=" + str(getLongAndLat().latitude) + "&longitude=" + str(getLongAndLat().longitude) + "&start_date=2013-03-14&end_date=2013-03-22&hourly=temperature_2m"


    response = requests.request("GET", url)

    print(response.text)

# Get average temperature between two dates x years between
def previousDateAverage():
    url = "https://archive-api.open-meteo.com/v1/archive?latitude=" + str(getLongAndLat().latitude) + "&longitude=" + str(getLongAndLat().longitude) + "&start_date=2013-03-14&end_date=2013-03-22&hourly=temperature_2m"


    response = requests.request("GET", url)

    print(response.text)


while not exitProgram:

    print("Welcome to the weather checker. What do you want to check? ")
    print("1. Check todays temperature forcast")
    print("2. Check weather temperature for x days forward")
    print("3. Check todays temperature weather x years ago")
    print("4. Check average temperature from date x to date y")
    choice = input("Option: ")

    timesToLoop = input("How many years back do you want to check the weather? ")

    while int(timesToLoop) > 10:
        timesToLoop = input("Can only check 10 years back. How many years back do you want to check? ")

    futureForcast()
