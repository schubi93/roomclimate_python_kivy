from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.config import Config

import Adafruit_DHT
import datetime
import requests
import json

Config.set('graphics', 'fullscreen', 'auto', 'show_cursor', 0)

DHT11_PIN = 4

class RaspiApp(App):

    def build(self):
        size_left = '100sp'
        layout = BoxLayout(padding=10, orientation = 'horizontal')
        layoutlinks = BoxLayout(orientation = 'vertical')
        self.time = Label(text='00:00', font_size=size_left)
        self.date = Label(text='00-XXX', font_size=size_left)
        self.week = Label(text='KW XX', font_size=size_left)
        layoutlinks.add_widget(self.time)
        layoutlinks.add_widget(self.date)
        layoutlinks.add_widget(self.week)
        layout.add_widget(layoutlinks)

        size_right = '60sp'
        layoutrechts = BoxLayout(orientation='vertical')
        self.temp_hum_in = Label(text = '99°C 100 %', font_size=size_right)
        self.temp_hum_out = Label(text = '99°C 100 %', font_size=size_right)
        self.feel_speed = Label(text = '99 km/h 99°C', font_size=size_right)
        self.pres = Label(text = '9999 Pa', font_size=size_right)
        layoutrechts.add_widget(self.temp_hum_in)
        layoutrechts.add_widget(self.temp_hum_out)
        layoutrechts.add_widget(self.feel_speed)
        layoutrechts.add_widget(self.pres)
        layout.add_widget(layoutrechts)

        self.change_values()
        Clock.schedule_interval(lambda dt: self.change_values(), 10)

        return layout

    def change_values(self):
        self.updatedtime()
        self.updatedht()
        self.updateweather()

    def updatedtime(self):
        now = datetime.datetime.now()
        self.date.text = now.strftime("%d-%b")
        self.time.text = now.strftime("%H:%M")
        self.week.text = 'KW ' + now.strftime("%V")
        return 0

    def updatedht(self):
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, DHT11_PIN)
        self.temp_hum_in.text = str(int(temperature)) + '°C / ' + str(int(humidity)) + '%'
        return 0

    def updateweather(self):
        api_key = "59ab5a2a045851451ddd0744020788cc"
        # Augsburg
        lat="48.327510"
        lon="10.894757"
        url = "https://api.openweathermap.org/data/2.5/onecall?lat=%s&lon=%s&appid=%s&units=metric" % (lat, lon, api_key)

        response = requests.get(url)
        data = json.loads(response.text)
        data_temp_is = round(data["current"]["temp"])
        data_temp_feel = round(data["current"]["feels_like"])
        data_speed = round(data["current"]["wind_speed"]*3.6)
        data_hum = round(data["current"]["humidity"])
        data_pres = round(data["current"]["pressure"])
        self.temp_hum_out.text = str(int(data_temp_is)) + '°C / ' + str(int(data_hum)) + '%'
        self.pres.text = str(data_pres) + ' Pa'
        self.feel_speed.text = str(int(data_temp_feel)) + '°C / ' + str(data_speed) +  ' kph'
if __name__ == "__main__":
    app = RaspiApp()
    app.run()