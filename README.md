# roomclimate_python_kivy

A project for a rasperry pi, written in python to display different room climate and showing a wet, sweating or freezing smiley.

## Ideas

This program was written to help a friend of mine with a moaning girlfriend. She was always complaining about a too hot or too cold flat.

## Program

By running main.py, the sensors get initialized and asked about their values in a loop. The values get displayed using kivy as GUI.

## Dependencies

```shell
pip3 install kivy
pip3 install Adafruit_DHT
pip3 install ntplib
```

## Autostart

Edit ` /etc/xdg/autostart/RPi-infoscreen.desktop` with

```
[Desktop Entry]
Type=Application
Name=RPi-infoscreen
Comment=Kivy RPI Infoscreen
NoDisplay=false
Exec=/usr/bin/lxterminal -e $(GIT_ROOT_DIR)/src/start_app.sh
NotShowIn=GNOME;KDE;XFCE;
```

## Schematic

**Note:** Still to come!

## Authors

* **Philipp Schubaur** - *Initial work*

## License

This project is licensed under the GNU GPLv3 License
