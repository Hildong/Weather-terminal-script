import requests
from geopy.geocoders import Nominatim 
from datetime import datetime
exitProgram = False

# Get longitude and latitude of requested city
def getLongAndLat():
    # Init Nominatim API
    geolocator = Nominatim(user_agent="TerminalWeatherApi")
    city = input("Please provide the city of temperature you want: ")

    return geolocator.geocode(city)

def printResultSpaces(space):
    print("\n" * space)
    print("----- ")
    print("\n" * space)

# Get todays forcast
def todaysForcast(lat, long):

    url = "https://api.open-meteo.com/v1/forecast?latitude=" + str(lat) + "&longitude=" + str(long) + "&hourly=temperature_2m"
    response = requests.request("GET", url).json()

    printResultSpaces(3)

    for i in range(24):
        print(response["hourly"]["time"][i] + ": " + str(response["hourly"]["temperature_2m"][i]))
    
    printResultSpaces(3)


# Get forcast for x amount of days forward
def futureForcast(lat, long):

    url = "https://api.open-meteo.com/v1/forecast?latitude=" + str(lat) + "&longitude=" + str(long) + "&hourly=temperature_2m"
    response = requests.request("GET", url).json()

    printResultSpaces(3)

    for i in range(len(response["hourly"]["time"])):
        print("\n") if i % 24 == 0 else None
        print(response["hourly"]["time"][i] + ": " + str(response["hourly"]["temperature_2m"][i]))
    
    printResultSpaces(3)

# Get average temperature of todays date x years back
def todaysAverage(lat, long):
    url = "https://api.open-meteo.com/v1/forecast?latitude=" + str(lat) + "&longitude=" + str(long) + "&hourly=temperature_2m"

    response = requests.request("GET", url).json()

    printResultSpaces(1)

    minTemp=maxTemp=minTempPos=maxTempPos = 0

    for i in range(len(response["hourly"]["time"])):
        if minTemp > response["hourly"]["temperature_2m"][i]:
            minTemp = response["hourly"]["temperature_2m"][i]
            minTempPos = i

        if maxTemp < response["hourly"]["temperature_2m"][i]:
            maxTemp = response["hourly"]["temperature_2m"][i]
            maxTempPos = i

    print("Min temperature today: \n" + response["hourly"]["time"][minTempPos] + ": " + str(minTemp))
    print("Max temperature today: \n" + response["hourly"]["time"][maxTempPos] + ": " + str(maxTemp))

    
    printResultSpaces(1)

# Get average temperature between two dates x years between
def previousDateAverage(lat, long):

    whatDate = input("What date do you want to check for? (format MM-DD) ")
    yearsBack = input("How many years back do you want to check the date for? ")

    url = "https://archive-api.open-meteo.com/v1/archive?latitude=" + str(lat) + "&longitude=" + str(long) + "&start_date=" + str(datetime.today().year - int(yearsBack)) + "-" + whatDate + "&end_date=" + str(datetime.today().year -1) + "-" + whatDate + "&hourly=temperature_2m"
    response = requests.request("GET", url).json()

    printResultSpaces(1)

    lowestTempAverage = 0.0
    highestTempAverage = 0.0
    lowestTemp = 0.0
    highestTemp = 0.0
    lowestTempDate = " "
    highestTempDate = " "
    temperatures = []
    hoursPerYearLooped = 0

    for i in range(len(response["hourly"]["time"])):
        #if response["hourly"]["time"][i]
        if response["hourly"]["time"][i][5:10] == whatDate:
            #print(min(response["hourly"]["temperature_2m"][i]))
            hoursPerYearLooped += 1
            if highestTemp < response["hourly"]["temperature_2m"][i]:
                highestTemp = response["hourly"]["temperature_2m"][i]
                highestTempDate = response["hourly"]["time"][i]

            if lowestTemp > response["hourly"]["temperature_2m"][i] or i == 1:
                lowestTemp = response["hourly"]["temperature_2m"][i]
                lowestTempDate = response["hourly"]["time"][i]

            if hoursPerYearLooped < 24:
                temperatures.append(response["hourly"]["temperature_2m"][i])
            else:
                lowestTempAverage += min(temperatures)
                highestTempAverage += max(temperatures)
                temperatures = []
                temperatures.append(response["hourly"]["temperature_2m"][i])
                hoursPerYearLooped = 1

    

    print("Lowest average temperature over the past " + yearsBack + " years on " + whatDate + ": " + str(lowestTempAverage/int(yearsBack)))
    print("Lowest temperature over the past " + yearsBack + " years on " + lowestTempDate + ": " + str(lowestTemp))
    print("Highest average temperature over the past " + yearsBack + " years on " + whatDate + ": " + str(highestTempAverage/int(yearsBack)))
    print("Highest temperature over the past " + yearsBack + " years on " + highestTempDate + ": " + str(highestTemp))


    
    printResultSpaces(1)


while not exitProgram:

    print("Welcome to the weather checker. What do you want to check? ")
    print("1. Check todays temperature forcast")
    print("2. Check weather temperature for x days forward")
    print("3. Check lowest and highest temperature weather x years ago")
    print("4. Check lowest and highest temperature from date x to date y")
    print("5. Exit")
    choice = input("Option: ")

    if choice == "1":
        location = getLongAndLat()
        todaysForcast(location.latitude, location.longitude)
    elif choice == "2":
        location = getLongAndLat()
        futureForcast(location.latitude, location.longitude)
    elif choice == "3":
        location = getLongAndLat()
        todaysAverage(location.latitude, location.longitude)
    elif choice == "4":
        location = getLongAndLat()
        previousDateAverage(location.latitude, location.longitude)
    elif choice == "5":
        exitProgram = True
    else:
        print("Not a valid option")
