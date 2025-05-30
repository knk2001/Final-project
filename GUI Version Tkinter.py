import tkinter as tk
import requests

API_KEY = 'c55aab85cd50a58314cbbeb9acf06c4e'


def get_weather_data():
    city = city_entry.get()
    if not city:
        result_label.config(text="Please enter a city name.")
        return

    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()

        if data.get("cod") != 200:
            result = f"Error: {data.get('message')}"
        else:
            weather = data['weather'][0]['description'].capitalize()
            temp = data['main']['temp']
            feels_like = data['main']['feels_like']
            humidity = data['main']['humidity']
            result = f"""
📍 {city}
Condition   : {weather}
Temperature : {temp}°C
Feels Like  : {feels_like}°C
Humidity    : {humidity}%
"""
        result_label.config(text=result)
    except Exception as e:
        result_label.config(text=f"Error: {str(e)}")


# GUI Setup
root = tk.Tk()
root.title("Weather Dashboard")

tk.Label(root, text="Enter City:", font=("Arial", 14)).pack(pady=5)
city_entry = tk.Entry(root, width=30, font=("Arial", 14))
city_entry.pack(pady=5)

tk.Button(root, text="Get Weather", command=get_weather_data, font=("Arial", 12)).pack(pady=10)

result_label = tk.Label(root, text="", font=("Arial", 12), justify="left")
result_label.pack(pady=10)

root.mainloop()