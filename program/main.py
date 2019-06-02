from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.label import Label
from kivy.clock import Clock
import smbus2
import time
import Adafruit_DHT

#from kivy.config import Config
#Config.set('graphics', 'fullscreen', 'auto')


class RaspiApp(App):

    def build(self):
        size = '100sp'
        layout = BoxLayout(padding=10, orientation = 'horizontal')
        layoutlinks = BoxLayout(orientation = 'vertical')
        layoutrechts = BoxLayout(orientation='vertical')
        self.img = Image(source = 'ok.png')
        self.temp = Label(text = '99°C', font_size=size)
        self.hum = Label(text='100 %', font_size=size)
        self.co2 = Label(text='1000 ppm CO²', font_size=size)
        self.lux = Label(text='1000 Lux', font_size=size)
        layoutlinks.add_widget(self.img)
        layoutrechts.add_widget(self.temp)
        layoutrechts.add_widget(self.hum)
        layoutrechts.add_widget(self.co2)
        layoutrechts.add_widget(self.lux)

        layout.add_widget(layoutlinks)
        layout.add_widget(layoutrechts)

        global bus
        bus = smbus2.SMBus(1)

        Clock.schedule_once(lambda dt: self.clocks(), 5)
        return layout

    def clocks(self):
        Clock.schedule_interval(lambda dt: self.change_values(), 2)

    def change_values(self):
        print('Start Event')
        update = False
        puffer = None
        puffer = self.abfragelicht()
        if puffer != None:
            update = True
            imgupdate = puffer
        puffer =''
        puffer = self.abfragedht()
        if puffer != None:
            update = True
            imgupdate = puffer
        puffer = None
        puffer = self.abfrageco2()
        if puffer != None:
            update = True
            imgupdate = puffer
        
        if update == False:
            self.img.source = 'ok.png'
        
        if update == True:
            self.img.source = imgupdate

    def abfragelicht(self):
        
        def convertToNumber(data):
            return ((data[1] + (256 * data[0])) / 1.2)

        def readLight():
            data = bus.read_i2c_block_data(0x23, 0x20, 0x02)
            return convertToNumber(data)

        lux = int((readLight()))
        self.lux.text = str(lux) + ' Lux'
        if lux < 400:
            bild = 'dunkel.png'        
            return bild

        

    def abfragedht(self):
        
        humidity, temperature = Adafruit_DHT.read_retry(Adafruit_DHT.DHT11, 24)
        
        self.hum.text = str(int(humidity)) + '%rel.'
        self.temp.text = str(int(temperature)) + '°C'
        
        if humidity > 60:
            bild = 'feucht.png'
            return bild
    
        elif temperature < 20:
            bild = 'kalt.png'
            return bild

        elif temperature > 24:
            bild = 'warm.png'
            return bild
        
       

    def abfrageco2(self):
        
        bus.write_i2c_block_data(0x58, 0x20, [0x03])
        time.sleep(1)
        bus.write_i2c_block_data(0x58, 0x20, [0x08])
        time.sleep(1)
        data = bus.read_i2c_block_data(0x58, 0, 0x02)
        #ppm = ((data[1] + (256 * data[0])) / 1.2)
        ppm = data[0] * 1000 + data[1]
        self.co2.text = str(int(ppm)) + ' ppm CO²'
        print(str(int(ppm)) + ' ppm CO²')
        if ppm > 1600:
            bild = 'co2.png'
            return bild
    
if __name__ == "__main__":
    app = RaspiApp()
    app.run()