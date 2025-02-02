# Name: Zaheer Safi
# Class: CS 341
# Date: 01/30/2024
# project: CTA Datbase App

import sqlite3
import matplotlib.pyplot as plt


##################################################################  

# print_stats
# Given a connection to the CTA database, executes various
# SQL queries to retrieve and output basic stats.

def print_stats(dbConn):
    
    dbCursor = dbConn.cursor()
        
    print("General Statistics:")

    query = """
    
    SELECT 
        (SELECT COUNT(*) FROM Stations) AS station_count,
        (SELECT COUNT(*) FROM Stops) AS stop_count,
        (SELECT COUNT(Num_Riders) FROM Ridership) AS ride_entries_count,
        (SELECT DATE(MAX(Ride_Date)) FROM Ridership) AS max_ride_date,
        (SELECT DATE(MIN(Ride_Date)) FROM Ridership) AS min_ride_date,
        (SELECT SUM(Num_Riders) FROM Ridership) AS total_ridership;
    """

    dbCursor.execute(query)
    row = dbCursor.fetchone()
    
    print(f"  # of stations: {row[0]:,}")
    print(f"  # of Stops: {row[1]:,}")
    print(f"  # of ride entries: {row[2]:,}")
    print(f"  Date range: {row[4]} - {row[3]}")
    print(f"  Total ridership: {row[5]:,}")


# take the user input Station Name from the user and find any matching Stations in the database and ouput
# all the info regarding the Station
def command1(dbConn):
    
    # take the user input
    print()
    command1_entry = input("Enter partial station name (wildcards _ and %): ")

    # sql query and store the result
    dbCursor = dbConn.cursor()
    query = "select * from Stations where Station_Name like ? order by Station_Name asc;"
    dbCursor.execute(query, (command1_entry,))
    result = dbCursor.fetchall()

    # if the stations were avaialble output them
    if result:
        for row in result:
            print(row[0], ":" ,row[1])            
    
    # else print the message
    else:
        print("**No stations found...")

# Given a station name, find the percentage of riders on weekdays, on Saturdays, and on
# Sundays/holidays for that station and output it to terminal.
def command2(dbConn):
    
    print()
    command2_entry = input("Enter the name of the station you would like to analyze: ")

    query = """
            select sum(Num_Riders) from Ridership 
            inner join Stations ON Stations.Station_ID = Ridership.Station_ID 
            where Stations.Station_Name = ?
            group by Type_Of_Day;
            
            """
    dbCursor = dbConn.cursor()
    dbCursor.execute(query, (command2_entry,))
    result = dbCursor.fetchall()
    
    if result:
        sum = 0
        for row in result:
            sum = sum + row[0]
        
        print(f"Percentage of ridership for the {command2_entry} station:")
        print(f"   Weekday ridership: {result[2][0]:,} ({result[2][0]/sum * 100:.2f}%)")
        print(f"   Saturday ridership: {result[0][0]:,} ({result[0][0]/sum * 100:.2f}%)")
        print(f"   Sunday/holiday ridership: {result[1][0]:,} ({result[1][0]/sum * 100:.2f}%)")
        print(f"   Total ridership: {sum:,}")
    
    else:
        print("**No data found...")

        
# Output the total ridership on weekdays for each station, with station names rather than
# the station IDs. Also show the percentages, taken out of the total ridership on weekdays
# for all the stations. Order the results in descending order by ridership
def command3(dbConn):
        
    print("Ridership on Weekdays for Each Station")

    query = """
            select Stations.Station_Name, sum(Num_Riders) as total from Ridership 
            inner join Stations ON Stations.Station_ID = Ridership.Station_ID 
            where Type_Of_Day = 'W'
            group by Stations.Station_Name
            order by total desc;
            
            """
    dbCursor = dbConn.cursor()
    dbCursor.execute(query)
    result = dbCursor.fetchall()
        
    sum = 0
    for row in result:
        sum = sum + row[1]

    for row in result:
        print(f"{row[0]} : {row[1]:,} ({row[1]/sum * 100:.2f}%)")


# Given a line color and direction, output all the stops for that line color in that direction.
# 
# Order by stop name in ascending order.
def command4(dbConn):

    print()
    line_entry_1 = input("Enter a line color (e.g. Red or Yellow): ")
    line_entry = line_entry_1.title()
    
    query1 = "select * from Lines where Color = ?;"
    dbCursor = dbConn.cursor()
    dbCursor.execute(query1, (line_entry,))
    result1 = dbCursor.fetchall()

    if not result1:
        print("**No such line...")
        return
    
    direction_entry_1 = input("Enter a direction (N/S/W/E): ")
    direction_entry = direction_entry_1.upper()

    query2 = "select * from Stops where Direction = ?;"
    dbCursor.execute(query2, (direction_entry,))
    result2 = dbCursor.fetchall()

    if not result2:
        print("**That line does not run in the direction chosen...")
        return
    
    query3 = """
            select Stop_Name, Direction, ADA from Stops 
            inner join StopDetails on StopDetails.Stop_ID = Stops.Stop_ID 
            inner join Lines on Lines.Line_ID = StopDetails.Line_ID
            where Lines.Color = ? and Stops.Direction = ?
            order by Stop_Name asc;
            """   
    dbCursor.execute(query3, (line_entry, direction_entry,))
    result3 = dbCursor.fetchall()

    if result3:
        for row in result3:
            if row[2] == 1:
                print(f"{row[0]} : direction = {row[1]} (handicap accessible)")
            else:
                print(f"{row[0]} : direction = {row[1]} (not handicap accessible)")

    else:
        print("**That line does not run in the direction chosen...")


# Output the number of stops for each line color, separated by direction. Show the results
# in ascending order by color name, and then in ascending order by direction. Also show
# the percentage for each one, which is taken out of the total number of stops.
def command5(dbConn):

    print("Number of Stops For Each Color By Direction")

    query1 = "select count(*) from Stops"
    dbCursor = dbConn.cursor()
    dbCursor.execute(query1)
    result1 = dbCursor.fetchone()

    query = """
            select Lines.Color, Stops.Direction, count(*) as total from Stops
            inner join StopDetails on StopDetails.Stop_ID = Stops.Stop_ID
            inner join Lines on Lines.Line_ID = StopDetails.Line_ID
            group by Lines.Color, Stops.Direction
            order by Lines.Color, Stops.Direction asc;
            """
    dbCursor.execute(query)
    result = dbCursor.fetchall()

    for row in result:
        print(f"{row[0]} going {row[1]} : {row[2]} ({row[2]/result1[0] * 100:.2f}%)")


# Given a station name, output the total ridership for each year for that station, in
# ascending order by year. Allow the user to use wildcards _ and % for partial names.
# Show an error message if the station name does not exist or if multiple station names
# match.
def command6(dbConn):
    
    print()
    Station_name = input("Enter a station name (wildcards _ and %): ")
    
    query = """
            select Stations.Station_Name, strftime('%Y', Ride_Date) as year, sum(Num_Riders) from Ridership
            inner join Stations on Stations.Station_ID = Ridership.Station_ID
            where Station_Name like ?
            group by year
            order by year asc;
            """
    dbCursor = dbConn.cursor()
    dbCursor.execute(query, (Station_name,))
    result = dbCursor.fetchall()

    if result:
        
        first_station_name = result[0][0]
        multiple_stations = False

        for row in result:
            if row[0] != first_station_name:
                multiple_stations = True
                break

        if multiple_stations:
            print("**Multiple stations found...")
            return
        
        else:
            print("Yearly Ridership at", first_station_name)
            for row in result:
                print(f"{row[1]} : {row[2]:,}")
    
    else:
        print("**No station found...")
        return

    print()
    plot_input = input("Plot? (y/n) ")

    if plot_input == 'y':
        
        years = [row[1] for row in result]
        number_of_riders = [row[2] for row in result]

        plt.figure(figsize=(12, 6))
        plt.plot(years, number_of_riders, marker='o')
        plt.title(f"Yearly Ridership at {first_station_name} Station")
        plt.xlabel('Year')
        plt.ylabel('Number of Riders')
        plt.show()

# function take a stations name as an argument and checks if a stations simialr to the entry is available in the database
# with the helf of like keyword and the % modifier and return true of false. if multiple or no stations were founch returns false
# otherwise returns true
def check_Station(dbConn, station_name) -> bool:
    
    query1 = """
            select Stations.Station_Name from Ridership
            inner join Stations on Stations.Station_ID = Ridership.Station_ID
            where Station_Name like ?;
            """
    dbCursor = dbConn.cursor()    
    dbCursor.execute(query1, (station_name,))
    result = dbCursor.fetchall()

    if result:
        
        first_station_name = result[0][0]
        multiple_stations = False

        for row in result:
            if row[0] != first_station_name:
                multiple_stations = True
                break

        if multiple_stations:
            print("**Multiple stations found...")
            return False
    
    else:
        print("**No station found...")
        return False
    
    return True


# this command Given a station name and year, output the total ridership for each month in that year.
# The user should be able to enter SQL wildcards (_ and %) for the station name.
def command7(dbConn):
    
    print()
    station_name = input("Enter a station name (wildcards _ and %): ")

    query1 = "select Station_Name from Stations where Station_Name like ?;"
    dbCursor = dbConn.cursor()
    dbCursor.execute(query1, (station_name,))
    result = dbCursor.fetchone()
    
    func_return = check_Station(dbConn, station_name)

    if func_return == False:
        return

    year = input("Enter a year: ")
    
    query = """
            select strftime("%m/%Y", Ride_Date) as date, sum(Num_Riders) as total, Stations.Station_Name from Ridership
            inner join Stations on Stations.Station_ID = Ridership.Station_ID
            where Stations.Station_Name like ? and strftime("%Y", Ride_Date) = ?
            group by date
            order by date asc;
            """
    dbCursor.execute(query, (station_name, year,))
    result1 = dbCursor.fetchall()

    print("Monthly Ridership at", result[0] , "for", year)
    if result1:    
        for row in result1:
            print(f"{row[0]} : {row[1]:,}")
        
    print()
    plot_input = input("Plot? (y/n) ")

    if plot_input == 'y':
        
        if result1:
            months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
            num_riders = [row[1] for row in result1]
        else:
            # If result is empty, both months and num_riders should be empty lists
            months = []
            num_riders = []

        plt.figure(figsize=(10,6))

        # Plotting the graph
        plt.plot(months, num_riders, marker='o')

        # Setting the title and labels
        plt.title(f"Monthly Ridership at {result[0]} Station for ({year})")
        plt.xlabel("Month")
        plt.ylabel("Number of Riders")

        # Display the graph
        plt.show()
        

# Given two station names and year, output the total ridership for each day in that year.
# The user should be able to enter SQL wildcards (_ and %) for each station name. Since
# the full output would be quite long, you should only output the first 5 days and last 5
# days of data for each station.
def command8(dbConn):
    
    print()
    year = input("Year to compare against? ")

    print()
    station1_name = input("Enter station 1 (wildcards _ and %): ")

    if check_Station(dbConn, station1_name) == False:
        return

    print()
    station2_name = input("Enter station 2 (wildcards _ and %): ")

    if check_Station(dbConn, station2_name) == False:
        return
    
    

    full_query = """
            select date(Ride_Date) as date, sum(Num_Riders), Stations.Station_ID, Stations.Station_Name from Ridership
            inner join Stations on Stations.Station_ID = Ridership.Station_ID
            where Stations.Station_Name like ? and strftime("%Y", Ride_Date) = ?
            group by Ride_Date
            order by date asc;
            """
    dbCursor = dbConn.cursor()
    dbCursor.execute(full_query, (station1_name, year,))
    result = dbCursor.fetchall()    
    dbCursor.execute(full_query, (station2_name, year,))
    result1 = dbCursor.fetchall()

    print("Station 1:", station1_name)
        
    
    if (result):
        
        for i in range(5):
            print(f"{result[i][0]} {result[i][1]}")
        
        last_rows = len(result) - 5

        for i in range(last_rows, len(result)):
            print(f"{result[i][0]} {result[i][1]}")
    
    print("Station 2:", station2_name)
        

    if (result1):

        
        for i in range(5):
            print(f"{result1[i][0]} {result1[i][1]}")

        for i in range(last_rows, len(result1)):
            print(f"{result1[i][0]} {result1[i][1]}")

        print()
    plot_input = input("Plot? (y/n) ")

    if plot_input == 'y':

        Days = [i for i in range(366)]
        num_riders_1 = []
        num_riders_2 = []

        if result:
            num_riders_1 = [row[1] for row in result]
            plt.plot(Days, num_riders_1, label=result[0][3])
        
        if result1:
            num_riders_2 = [row[1] for row in result1]
            plt.plot(Days, num_riders_1, label=result[0][3])

        plt.figure(figsize=(10,6))
        
        plt.plot(Days, num_riders_1, label=result[0][3])

        # Plotting num_riders_2 in orange
        plt.plot(Days, num_riders_2, color='orange', label=result1[0][3])

        plt.ylabel("Number of Riders")
        plt.xlabel("Days")
        plt.title(f"Ridership Each Day for {year}")

        # Adding a legend
        plt.legend()
        plt.show()

# Given a set of latitude and longitude from the user, find all stations within a mile square
# radius around the the given latitude and longitude but the latitude has to be between 43 and 40 and the longitude
# has to be between -88 and -87 this way we always stay in chicago      
def command9(dbConn):
    
    print()
    latitude = float(input("Enter a latitude: "))
    
    # Check if the latitude and longitude are within the bounds of Chicago
    if (latitude > 43) or (latitude < 40):
        print("**Latitude entered is out of bounds...")
        return
    
    longitude = float(input("Enter a longitude: "))
    
    if not (-88 <= longitude <= -87):
        print("**Longitude entered is out of bounds...")
        return


    # Each degree of latitude is approximately 69 miles apart
    # Each degree of longitude in Chicago is approximately 51 miles apart
    lat_mile = 1 / 69
    lon_mile = 1 / 51

    # Calculate the latitude and longitude boundaries for a square mile radius
    lat_lower_bound = round(latitude - lat_mile, 3)
    lat_upper_bound = round(latitude + lat_mile, 3)
    lon_lower_bound = round(longitude - lon_mile, 3)
    lon_upper_bound = round(longitude + lon_mile, 3)

    # SQL query to find stations within these bounds
    query = """
            SELECT DISTINCT Stations.Station_Name, Stops.Latitude, Stops.Longitude
            FROM Stations
            INNER JOIN Stops ON Stations.Station_ID = Stops.Station_ID
            WHERE Stops.Latitude BETWEEN ? AND ?
            AND Stops.Longitude BETWEEN ? AND ?
            
            order by Stations.Station_Name asc;
            """
    dbCursor = dbConn.cursor()
    dbCursor.execute(query, (lat_lower_bound, lat_upper_bound, lon_lower_bound, lon_upper_bound))
    results = dbCursor.fetchall()

    if results:
        print()
        print("List of Stations Within a Mile")
        for row in results:
            print(f"{row[0]} : ({row[1]}, {row[2]:})")
        
    else:
        print("**No stations found...")
        return
    
    print()
    plot_input = input("Plot? (y/n) ")

    if plot_input == 'y':
        
        image = plt.imread("chicago.png")
        xydims = [-87.9277, -87.5569, 41.7012, 42.0868]  # area covered by the image

        plt.figure(figsize=(8, 6))

        plt.imshow(image, extent=xydims)
        plt.title("Stations near you")

        # Assuming x and y are lists of longitude and latitude respectively
        # If not, you need to create them from the 'results' data
        x = [row[2] for row in results]
        y = [row[1] for row in results]

        plt.plot(x, y)  

        # Annotate each (x, y) coordinate with its station name
        for row in results:
            plt.annotate(row[0], (row[2], row[1]))

        plt.xlim([-87.9277, -87.5569])
        plt.ylim([41.7012, 42.0868])
        plt.show()
    


##################################################################  
#
# main
#
print('** Welcome to CTA L analysis app **')
print()

#open the database and print the the general stats regarding it
dbConn = sqlite3.connect('CTA2_L_daily_ridership.db')

print_stats(dbConn)
print()

user_input = 'n'

# take the user input and execute the commands accordingly
while (user_input != 'x'):
    
    user_input = input("Please enter a command (1-9, x to exit): ")
    
    if ((not user_input.isdigit() or int(user_input) < 1 or int(user_input) > 9) and (user_input != 'x')):
        print("**Error, unknown command, try again...")
    
    if (user_input.isdigit() and int(user_input) == 1):
        command1(dbConn)
    
    if (user_input.isdigit() and int(user_input) == 2):
        command2(dbConn)
    
    if (user_input.isdigit() and int(user_input) == 3):
        command3(dbConn)
    
    if (user_input.isdigit() and int(user_input) == 4):
        command4(dbConn)
    
    if (user_input.isdigit() and int(user_input) == 5):
        command5(dbConn)
    
    if (user_input.isdigit() and int(user_input) == 6):
        command6(dbConn)
    
    if (user_input.isdigit() and int(user_input) == 7):
        command7(dbConn)
    
    if (user_input.isdigit() and int(user_input) == 8):
        command8(dbConn)
    
    if (user_input.isdigit() and int(user_input) == 9):
        command9(dbConn)

    print()
    

dbConn.close()

