# PWM Fan Control for Raspberry Pi 4

[Deutsches Readme](https://github.com/Hofei90/pwm_fan_control_pi4/blob/master/README_GERMAN.md)

__Beware, this is a rudimentairy implementation. Further features are planned, 
see [GitHub Project Board - Features](https://github.com/Hofei90/pwm_fan_control_pi4/projects/1)__

## Hardware
A hardware schematic could be found in the folder 'doc'
It is recommended to use a CMOS converter for the PWM line.
To keep it easy this converter is currently not part of the schematic.
Is the signal line used without converter the measured current was for me 255,5µA.
There is no guarntee that the Raspberry Pi will not destroyed (may over time).

## Software prepration
### Python
The scripts requires Python >= 3.6

### Installation pigpio
A manually installtion is required due to a old version in the repository is available which will not works with Raspberry Pi 4 and Buster.

Used pigpio Version: 70

For installation it can be used 'Method 2' form the official home page: http://abyz.me.uk/rpi/pigpio/download.html

### Installation Python modules
The requirements.txt contains all required Python modules. All listed modules can be used with 
install the following command:

`pip3 install --user -r requirements.txt`

### Config file modifications
The desired fan behaviour could be defined via the file `config.toml`.

## Setup Autostart
Copy all files (\*.service) from folder 'Systemd Service Unit Files' to /etc/systemd/system.

If the fan controller python script are NOT located in '/home/pi/pwm_fan_control_pi4/' the .service-files must be adjusted!

Modfiy the access rights for the systmd files as following

`chown root:root /etc/systemd/system/fan_control.service /etc/systemd/system/pigpiod.service`

`chmod 644 /etc/systemd/system/fan_control.service /etc/systemd/system/pigpiod.service`

## Test
Execute the following command and check with top or htop that the service is running
`systemctl start fan_control.service`

If everything works as expected enable the autostart for the fan controller
`systemctl enable fan_control.service`
