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
    
    # Texts to return
    
    if df["temp"].max() >= 30.0 :
        TEMP = f'- La temperatura  máxima, media y mínima va a ser de {df["temp"].max():.1f} °C, {df["temp"].mean():.1f} °C y {df["temp"].min():.1f} °C. Yo que vos me pongo algo fresco y me mantengo hidratado.'

    elif df["temp"].min() <= 10.0 :
        TEMP = f'- La temperatura  máxima, media y mínima va a ser de {df["temp"].max():.1f} °C, {df["temp"].mean():.1f} °C y {df["temp"].min():.1f} °C. Abrigate! Yo que vos me pongo ese buzito que tanto te gusta.'

    else:
        TEMP = f'- La temperatura  máxima, media y mínima va a ser de {df["temp"].max():.1f} °C, {df["temp"].mean():.1f} °C y {df["temp"].min():.1f} °C.'


    HUMIDITY = f'- La humedad va estar entre {df["humidity"].min()}% y {df["humidity"].max()}%.'
    
    if (df["POP"] == 0).all() == True:
        
        POP = "- No esta previsto que llueva."
    
    else:
        
        POP = f'- La maxima probabilidad de lluvia es del {df["POP"].max()} % a las {df["POP"].idxmax().strftime("%H:%M")} hs. Si salis, te recomiendo que lleves una campera o un paraguas.'
        
    
    SUNRISE_SUNSET = f'Además, te cuento que hoy amaneció a las {(datetime.datetime.fromtimestamp(x["city"]["sunrise"]) - pd.offsets.Hour(3)).strftime("%H:%M")} hs y que va a oscurecer a las {(datetime.datetime.fromtimestamp(x["city"]["sunset"]) - pd.offsets.Hour(3)).strftime("%H:%M")} hs.'
    

    return 'En las proximas 24 hs se espera lo siguiente: ' + '\n' + TEMP + '\n' +  HUMIDITY + '\n' + POP + '\n' + SUNRISE_SUNSET

# get_ow_forecast()

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)


