import tkinter as tk
from datetime import datetime
import requests

#set up the main window 
root = tk.Tk()
root.title("Smart Weather Dashboard")
root.geometry("800x600")
root.configure(bg="black")

#grid spacing equal, -------row 0 row 1 ------- column 0 column 1
root.grid_rowconfigure(0, weight=1)
root.grid_rowconfigure(1, weight=1)
root.grid_columnconfigure(0, weight=1)
root.grid_columnconfigure(1, weight=1)

#four frames for the four quadrants of the dashboard
frame_time = tk.Frame(root, bg="black")       #top left
frame_sys = tk.Frame(root, bg="blue")         #top right
frame_weather = tk.Frame(root, bg="green")    #bottom left
frame_calendar = tk.Frame(root, bg="yellow")  #bottom right

#placement of the frames using coords
frame_time.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
frame_sys.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
frame_weather.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
frame_calendar.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

#dynamic functions with clock
def update_clock():
    #fetch the current time and date
    current_time = datetime.now().strftime("%H:%M:%S")
    current_date = datetime.now().strftime("%A, %d %B %Y")

    #update the label text with fstring for seperate lines
    label_time.config(text=f"{current_time}\n{current_date}")


    root.after(1000, update_clock)  


#------------------------- update weather with openmeteo API -------------------------#
def update_weather():
    #fetch the weather for leicester - Lat: 52.63, Lon: -1.13
    url = "https://api.open-meteo.com/v1/forecast?latitude=52.63&longitude=-1.13&current=temperature_2m"

    try:
        response = requests.get(url)
        data = response.json()

        current_temp = data['current']['temperature_2m']


        label_weather.config(text=f"Leicester\n{current_temp}°C")
    except Exception as e:
        label_weather.config(text="Weather Info\nError fetching data")
        print(f"Error fetching weather data: {e}")

    root.after(60000, update_weather)  #update every 60 seconds

#------------------------------------ Testing/Production Code ------------------------------------#

#placeholder label for time frame
label_time = tk.Label(frame_time, text="Time and Date", fg="white", bg="black", font=("Helvetica", 24))
label_time.pack(expand=True)

label_sys = tk.Label(frame_sys, text="System Info", fg="white", bg="blue", font=("Helvetica", 24))
label_sys.pack(expand=True)

label_weather = tk.Label(frame_weather, text="Weather Info", fg="white", bg="green", font=("Helvetica", 24))
label_weather.pack(expand=True)

label_calendar = tk.Label(frame_calendar, text="Calendar", fg="white", bg="yellow", font=("Helvetica", 24))
label_calendar.pack(expand=True)



update_clock()
update_weather()  #initial call to start the clock update loop
# keep it running
root.mainloop()



