import json 
import requests
import pandas as pd
import numpy as np
import datetime
from flask import Flask
import os

api_key = "cadad626f98ae037eae33b8e5f4af1dc" # Open Weather API Key
city_name = "Buenos Aires"
units = "metric"
lang = "sp"
n_timesteps = 9

app = Flask(__name__)


@app.route('/')
def get_ow_forecast():
	
	url = f"https://api.openweathermap.org/data/2.5/forecast?&q={city_name}&cnt={n_timesteps}&units={units}&lang={lang}&appid={api_key}"

	response = requests.get(url)
	 
	x = response.json()

	# Crear un DF con las variables de interés

	datetimes_utc_0 = [x["list"][i]["dt_txt"] for i in range(n_timesteps)]

	datetimes_utc_arg = [datetime.datetime.strptime(i, "%Y-%m-%d %H:%M:%S") - pd.offsets.Hour(3) for i in datetimes_utc_0]

	# Get TEMPERATURA
	temps = ["%.1f" % x["list"][i]["main"]["temp"] for i in range(n_timesteps)]

	# Get SENSACIÓN TÉRMICA 
	feels_like = ["%.1f" % x["list"][i]["main"]["feels_like"] for i in range(n_timesteps)]

	# Get HUMIDITY
	humidity = [x["list"][i]["main"]["humidity"] for i in range(n_timesteps)]

	# Get CLOUDINESS (as a %)
	cloudiness = [x["list"][i]["clouds"]["all"] for i in range(n_timesteps)]

	# Get Ppt. probability (as a %) [POP]
	pop = [x["list"][i]["pop"] for i in range(n_timesteps)]

	# Dataframe columns
	df_cols = ["temp", "feels_like", "humidity", "cloudiness", "POP"]

	# Create DF
	df = pd.DataFrame(list(zip(temps, feels_like, humidity, cloudiness, pop)), columns=df_cols, index=datetimes_utc_arg)

	# Turn all columns to numeric
	df = df.apply(pd.to_numeric)

	return f'La temperatura media para hoy es {df["temp"].mean():.1f} °C.'


# get_ow_forecast()

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)


