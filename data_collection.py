import requests as rq

from secrets.key import key

url = f"https://api.openweathermap.org/data/2.5/weather?lat=52.520008&lon=13.4050&appid={key}"

resp = rq.get(url)