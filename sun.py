'''
Author: YHR
Description: This code generates the sunrise and sunset times of any given coordinates for every day over 365 days in seconds.
'''

import tkinter as tk
from PIL import Image, ImageTk

import datetime
from suntime import Sun, SunTimeException

root = tk.Tk()

canvas = tk.Canvas(root, width=500, height=500)

logo = Image.open('img/logo.png')
logo = ImageTk.PhotoImage(logo)
root.iconphoto(False, logo)
logo_label = tk.Label(image=logo)
logo_label.image = logo
logo_label.grid(columnspan=5, column=0, row=0)

instructions = tk.Label(
    root, text="Enter latitude and longitude of the city and the amount of seconds to add or remove from sunrise and sunset.", font=("Arial", 18), pady=50, padx=50)
instructions.grid(columnspan=2, column=1, row=1)

lat_input = tk.DoubleVar()
long_input = tk.DoubleVar()
add_seconds_to_sunrise = tk.IntVar()
add_seconds_to_sunset = tk.IntVar()
city_name = tk.StringVar()

lat_label = tk.Label(root, text='Latitude', font=('Ariel', 16, 'bold'))
lat_entry = tk.Entry(root, textvariable=lat_input,
                     font=('Ariel', 16, 'normal'), bg='#A9C386')
long_label = tk.Label(root, text='Longitude',
                      font=('Ariel', 16, 'bold'), pady=10)
long_entry = tk.Entry(root, textvariable=long_input,
                      font=('Ariel', 16, 'normal'), bg='#A9C386')

add_seconds_to_sunrise_label = tk.Label(
    root, text='Add seconds to sunrise (use negative values to remove seconds for example "-600")', font=('Ariel', 16, 'bold'))
add_seconds_to_sunrise_entry = tk.Entry(
    root, textvariable=add_seconds_to_sunrise, font=('Ariel', 16, 'normal'), bg='#A9C386')
add_seconds_to_sunset_label = tk.Label(
    root, text='Add seconds to sunset (use negative values to remove seconds for example "-600")', font=('Ariel', 16, 'bold'))
add_seconds_to_sunset_entry = tk.Entry(
    root, textvariable=add_seconds_to_sunset, font=('Ariel', 16, 'normal'), bg='#A9C386')

city_name_label = tk.Label(
    root, text='City Name', font=('Ariel', 16, 'bold'))
city_name_entry = tk.Entry(
    root, textvariable=city_name, font=('Ariel', 16, 'normal'), bg='#A9C386')


def getYearSun(lat, long, seconds_added_to_sunrise, seconds_added_to_sunset, city):
    sun = Sun(lat, long)

    # yearTimes = [0] # This array contains all the times in a tuple.
    yearTimes = []
    monthTimes = []

    # This array is required to loop correctly over the months.
    numOfDaysofMonths = [0, 31, 29, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]

    for i in range(1, 13):  # Loops over months
        #monthTimes.append((0, 0))
        # Loops over days of month
        for j in range(1, numOfDaysofMonths[i] + 1):
            if (j == 29):
                tempDate = datetime.date(2021, i, j-1)
                sunRise = sun.get_local_sunrise_time(tempDate)
                sunSet = sun.get_local_sunset_time(tempDate)
                sunRiseInSeconds = sunRise.hour * 60 * 60 + \
                    sunRise.minute * 60 + seconds_added_to_sunrise  # seconds added to sunset
                sunSetInSeconds = sunSet.hour * 60 * 60 + sunSet.minute * \
                    60 + seconds_added_to_sunset  # seconds added to sunset
                monthTimes.append((sunRiseInSeconds, sunSetInSeconds))
            else:
                tempDate = datetime.date(2021, i, j)
                sunRise = sun.get_local_sunrise_time(tempDate)
                sunSet = sun.get_local_sunset_time(tempDate)
                sunRiseInSeconds = sunRise.hour * 60 * 60 + \
                    sunRise.minute * 60 + seconds_added_to_sunrise  # seconds added to sunset
                sunSetInSeconds = sunSet.hour * 60 * 60 + sunSet.minute * \
                    60 + seconds_added_to_sunset  # seconds added to sunset
                monthTimes.append((sunRiseInSeconds, sunSetInSeconds))
        yearTimes.append(monthTimes)
        monthTimes = []

    # Change the cityName to proper city name.
    with open(city + ".txt", "w") as outfile:
        outfile.write(", ".join(str(item) for item in yearTimes))

    line = ''
    with open(city + ".txt", "r") as outfile:
        line = list(outfile.readline())
        for i in range(len(line)):
            if line[i] == "(":
                line[i] = '{'
            if line[i] == ')':
                line[i] = '}'

    # Change the cityName to proper city name.
    with open(city + ".txt", "w") as outfile:
        line = "".join(str(char) for char in line)
        outfile.write(line)

    return yearTimes


def write_file():
    lat = lat_input.get()
    long = long_input.get()
    seconds_added_to_sunrise = add_seconds_to_sunrise.get()
    seconds_added_to_sunset = add_seconds_to_sunset.get()
    city = city_name.get()

    yt = getYearSun(lat, long, seconds_added_to_sunrise,
                    seconds_added_to_sunset, city)

    lat_input.set(0.0)
    long_input.set(0.0)
    add_seconds_to_sunrise.set(0)
    add_seconds_to_sunset.set(0)
    city_name.set('')


generate_file = tk.Button(
    root, text='Generate File with Times', command=write_file, font=('Ariel', 18, 'bold'), bg='#222211', fg='white')

lat_label.grid(column=1, row=2)
lat_entry.grid(column=2, row=2)
long_label.grid(column=1, row=3)
long_entry.grid(column=2, row=3)
add_seconds_to_sunrise_label.grid(column=1, row=4)
add_seconds_to_sunrise_entry.grid(column=2, row=4)
add_seconds_to_sunset_label.grid(column=1, row=5)
add_seconds_to_sunset_entry.grid(column=2, row=5)
city_name_label.grid(column=1, row=6)
city_name_entry.grid(column=2, row=6)

generate_file.grid(columnspan=2, column=1, row=7)

root.mainloop()
