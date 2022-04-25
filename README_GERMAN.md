# PWM Fan Control for Raspberry Pi 4

__Achtung, das ist bisher nur ein sehr rudimentärer Code, weitere geplanten Features siehe unter 
[GitHub Project Board - Features](https://github.com/Hofei90/pwm_fan_control_pi4/projects/1)__

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
Getestete pigpio Version: 79

Zum Installieren folgenden Befehl ausführen:

`apt update && apt install pigpio python3-pigpio`

### Installation Pythonmodule
In der requirements.txt sind alle benötigten Pythonmodule enthalten. Alle aufgeführten Module lassen sich mit 
folgendem Befehl installieren:

`pip3 install --user -r requirements.txt`

### Configdatei anpassen
Das Verhalten des Lüfters lässt sich in der Datei `config.toml` definieren und wenn gewünscht anpassen.

## Einrichtung Autostart
Die im Ordner enthaltenden \*.service Files nach /etc/systemd/system kopieren.

Die Pfade in den Files sind ggf. der Umgebung anzupassen

Rechte der Systemd Files anpassen

`chown root:root /etc/systemd/system/fan_control.service /etc/systemd/system/pigpiod.service`

`chmod 644 /etc/systemd/system/fan_control.service /etc/systemd/system/pigpiod.service`

## Test
Anschließend händisch testen, nach Ausführen des Befehls sollte das Skript gestartet sein, überprüfbar z.B mit htop

`systemctl start fan_control.service`

Funktioniert alles wie gewünscht wird mit folgendem Befehl der Autostart aktiviert

`systemctl enable fan_control.service`
