import openmeteo_requests
import requests_cache
from retry_requests import retry
import pandas as pd

class ApiController:
    def __init__(self):
        self.url = "https://api.open-meteo.com/v1/forecast"
        self.params = {
                'hourly': ["temperature_2m", "precipitation", "rain", "weather_code", "cloud_cover", 
                           "cloud_cover_low", "cloud_cover_mid", "cloud_cover_high", "cloud_cover_2m", 
                           "wind_speed_10m", "wind_speed_50m", "wind_direction_10m", "wind_direction_50m", "wind_gusts_10m"],
                'models':  "dmi_seamless"
            } 
        # Setup the Open-Meteo API client with cache and retry on error
        cache_session = requests_cache.CachedSession('.cache', expire_after = 3600)
        retry_session = retry(cache_session, retries = 5, backoff_factor = 0.2)
        self.openmeteo = openmeteo_requests.Client(session = retry_session)
    
    def retrive_data(self, latlong):
        #latlong is a dict of latitude and longitude 
        request_params = dict(latlong, **self.params) 
        responses = self.openmeteo.weather_api(self.url, params=request_params)

        # Could be remodeled for making an API Call for multiple locations at the same time
        response = self.to_df(responses[0])
        return response
    

    def to_df(self, response):
        hourly = response.Hourly()
        variables = [
            "temperature_2m", "precipitation", "rain", "weather_code", "cloud_cover",
            "cloud_cover_low", "cloud_cover_mid", "cloud_cover_high", "cloud_cover_2m",
            "wind_speed_10m", "wind_speed_50m", "wind_direction_10m", "wind_direction_50m",
            "wind_gusts_10m"
        ]
        
        hourly_data = {
            "date": pd.date_range(
                start=pd.to_datetime(hourly.Time(), unit="s", utc=True),
                end=pd.to_datetime(hourly.TimeEnd(), unit="s", utc=True),
                freq=pd.Timedelta(seconds=hourly.Interval()),
                inclusive="left"
            )
        }
        
        for i, var in enumerate(variables):
            hourly_data[var] = hourly.Variables(i).ValuesAsNumpy()
        
        hourly_dataframe = pd.DataFrame(data=hourly_data)
        hourly_dataframe["day"] = hourly_dataframe["date"].apply(lambda x: x.strftime('%Y-%m-%d'))
        hourly_dataframe["hour"] = hourly_dataframe["date"].apply(lambda x: x.strftime('%H'))

        for var in variables:
            hourly_dataframe[var] = hourly_dataframe[var].round(2)
        
        return hourly_dataframe
