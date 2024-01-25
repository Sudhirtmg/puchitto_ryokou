from django.shortcuts import render

# Create your views here.
import requests


from django.shortcuts import render
import urllib.request
import json
# Create your views here.
def get_weather(prefecture):
   
        # print(city)
   api_url = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q=' + prefecture + '&units=metric&appid=4c2d74ed5caa623910b1ca93a9d3d8b9').read()
   api_data = json.loads(api_url)

   data = {
    "都道府県": prefecture,
    "country": api_data['sys']['country'],
    "天気の説明": api_data['weather'][0]['description'],
    "気温": api_data['main']['temp'],
    "気圧": api_data['main']['pressure'],
    "湿度": api_data['main']['humidity'],
    "天気アイコン": api_data['weather'][0]['icon'],
}
   return f'city: {prefecture}, data :{data}'
    
    
