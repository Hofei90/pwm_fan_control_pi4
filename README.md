# pwm_fan_control_pi4

__Achtung, das ist bisher nur ein sehr rudimentärer Code, weitere geplanten Features siehe unter Projekte__

## Hardware
Die Hardwareverkabelung ist unter dem Ordner doc zu finden.
Es ist zu empfehlen einen CMOS Konverter in die PWM Leitung einzubauen. Der Einfachheit zu Liebe, habe ich jedoch darauf 
verzichtet.
Die Signalleitung beanspruchte  bei Direktanschluss bei mir 255,5 µA. Keine Garantie aber, dass der Pi nicht doch
schaden deswegen nehmen kann.

## Vorbereitungen Software
### Python
Das Skript benötigt Python >=3.6

### Installation pigpio
Zunächst muss pigpio manuell installiert werden, da in dem Repository eine zu alte Version enthalten ist, welche nicht
mit dem Raspberry Pi 4 und Buster funktionierte.

Meine pigpio Version: 70

Installiert nach Methode 2 auf folgender offiziellen Seite: http://abyz.me.uk/rpi/pigpio/download.html

### Installation Pythonmodule
`pip3 install --user toml`

`pip3 install --user gpiozero`

### Configdatei anpassen
Das Verhalten des Lüfters lässt sich in der Datei `config.toml` definieren und wenn gewünscht anpassen. 
   
## Einrichtung Autostart
Die im Ordner enthaltenden *.service Files nach /etc/systemd/system kopieren.

Die Pfade in den Files sind ggf. der Umgebung anzupassen

Rechte der Systemd Files anpassen

`chown root:root /etc/systemd/system/fan_control.service /etc/systemd/system/pigpiod.service`

`chmod 644 /etc/systemd/system/fan_control.service /etc/systemd/system/pigpiod.service`

Anschließend händisch testen, nach Ausführen des Befehls sollte das Skript gestartet sein, überprüfbar z.B mit htop

`systemctl start fan_control.service`

Funktioniert alles wie gewünscht wird mit folgendem Befehl der Autostart aktiviert

`systemctl enable fan_control.service`

