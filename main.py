import code
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
frame_time = tk.Frame(root, bg="#202124")       #top left
frame_sys = tk.Frame(root, bg="#202124")         #top right
frame_weather = tk.Frame(root, bg="#202124")    #bottom left
frame_calendar = tk.Frame(root, bg="#202124")  #bottom right

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

#function to get weather condition such as sunny/cloudy/rainy/snowy etc
def get_weather_condition(code):
    if code == 0:
        return "Clear", "☀️"
    elif code in [1, 2, 3]:
        return "Cloudy", "☁️"
    elif code in [45, 48]:
        return "Foggy", "🌫️"
    elif code in [51, 53, 55, 61, 63, 65]:
        return "Rainy", "🌧️"
    elif code in [71, 73, 75]:
        return "Snowy", "❄️"
    elif code in [95, 96, 99]:
        return "Thunderstorm", "⛈️"
    return "Varying", "🌤️"

def update_weather():
    #fetch the weather for leicester - Lat: 52.63, Lon: -1.13
    url = "https://api.open-meteo.com/v1/forecast?latitude=52.63&longitude=-1.13&current=temperature_2m,weather_code&hourly=temperature_2m,weather_code&forecast_days=2"

    try:
        response = requests.get(url)
        data = response.json()

        #find the current temp
        current_temp = data['current']['temperature_2m']

        #find the current hour of the day 
        current_hour = datetime.now().hour

        #current weather condition code
        weather_code = data['current']['weather_code']
        condition, emoji = get_weather_condition(weather_code)

        #get the next 3 hours of temperature data
        hr1 = round(data['hourly']['temperature_2m'][current_hour + 1])
        hr2 = round(data['hourly']['temperature_2m'][current_hour + 2])
        hr3 = round(data['hourly']['temperature_2m'][current_hour + 3])

        code1 = data['hourly']['weather_code'][current_hour + 1]
        code2 = data['hourly']['weather_code'][current_hour + 2]
        code3 = data['hourly']['weather_code'][current_hour + 3]

        text1, icon1 = get_weather_condition(code1)
        text2, icon2 = get_weather_condition(code2)
        text3, icon3 = get_weather_condition(code3)


        #find the clock times for the forecasted hours
        time1 = f"{(current_hour + 1) % 24:02d}:00"
        time2 = f"{(current_hour + 2) % 24:02d}:00"
        time3 = f"{(current_hour + 3) % 24:02d}:00"

        #styling for the display text
        label_weather_temp.config(text=f"{round(current_temp)}°C")
        label_weather_icon.config(text=emoji)
        label_weather_condition.config(text=condition)

        forecast_string = f"{time1}   |   {time2}   |   {time3}\n{icon1} {hr1}°C   |   {icon2} {hr2}°C   |   {icon3} {hr3}°C"
        label_weather_forecast.config(text=forecast_string)

    except Exception as e:
        label_weather_temp.config(text="Error")
        label_weather_condition.config(text="Error")
        label_weather_forecast.config(text="Error fetching data")
        print(f"Weather error: {e}")

    root.after(300000, update_weather)  #update every 5 mins

#------------------------------------ Testing/Production Code ------------------------------------#

#placeholder label for time frame
label_time = tk.Label(frame_time, text="Time and Date", fg="white", bg="black", font=("Helvetica", 24))
label_time.pack(expand=True)


label_sys = tk.Label(frame_sys, text="System Info", fg="white", bg="blue", font=("Helvetica", 24))
label_sys.pack(expand=True)



# Bottom left Weather frames
label_weather_location = tk.Label(frame_weather, text="Leicester, UK", fg="#9aa0a6", bg="#202124", font=("Helvetica", 14))
label_weather_location.pack(pady=(20,0))

label_weather_temp = tk.Label(frame_weather, text="Temperature", fg="white", bg="#202124", font=("Helvetica", 56, "bold"))
label_weather_temp.pack()

label_weather_icon = tk.Label(frame_weather, text="--", fg="white", bg="#202124", font=("Helvetica", 64))
label_weather_icon.pack(pady=(5, 0))

label_weather_condition = tk.Label(frame_weather, text="Condition", fg="white", bg="#202124", font=("Helvetica", 24))
label_weather_condition.pack()

label_weather_forecast = tk.Label(frame_weather, text="Forecast", fg="white", bg="#202124", font=("Helvetica", 14))
label_weather_forecast.pack(pady=(20,0))





label_calendar = tk.Label(frame_calendar, text="Calendar", fg="white", bg="yellow", font=("Helvetica", 24))
label_calendar.pack(expand=True)



update_clock()
update_weather() 
# keep it running
root.mainloop()



