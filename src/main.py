from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.clock import Clock
import time
import Adafruit_DHT

from kivy.config import Config
Config.set('graphics', 'fullscreen', 'auto')


class RaspiApp(App):

    def build(self):
        size = '100sp'
        layout = BoxLayout(padding=10, orientation = 'horizontal')
        layoutlinks = BoxLayout(orientation = 'vertical')
        layoutrechts = BoxLayout(orientation='vertical')
        self.img = Image(source = '../img/ok.png')
        self.temp = Label(text = '99°C', font_size=size)
        self.hum = Label(text='100 %', font_size=size)
        layoutlinks.add_widget(self.img)
        layoutrechts.add_widget(self.temp)
        layoutrechts.add_widget(self.hum)

        layout.add_widget(layoutlinks)
        layout.add_widget(layoutrechts)

        Clock.schedule_once(lambda dt: self.clocks(), 5)
        return layout

    def clocks(self):
        Clock.schedule_interval(lambda dt: self.change_values(), 2)

    def change_values(self):
        update = False
        imgupdate = self.abfragedht()
        if imgupdate:
            update = True
            self.img.source = imgupdate
            return

        if update == False:
            self.img.source = '../img/ok.png'


    def abfragedht(self):

        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 4)

        self.hum.text = str(humidity) + '%rel.'
        self.temp.text = str(temperature) + '°C'

        if humidity > 60:
            bild = '../img/feucht.png'
            return bild

        elif temperature < 20:
            bild = '../img/kalt.png'
            return bild

        elif temperature > 28:
            bild = '../img/warm.png'
            return bild
        else:
            return 0

if __name__ == "__main__":
    app = RaspiApp()
    app.run()