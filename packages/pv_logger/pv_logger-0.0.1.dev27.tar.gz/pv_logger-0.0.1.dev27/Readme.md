# Python PV Logger

Logging of photovoltaic inverters
* to local cache (sqlite)
* to InfluxDB (can be remote over ssh)

## Kaco over RS485

```
pip install pv_logger
```

create a config file `config.yaml`:
```
archive_older_than_days: 30
# path to sqlite database
# change to file for permanent storage (!!)
engine: "sqlite:///:memory:"
influx:
  dbname: pv-nodes
  host: localhost
  password: no-need
  port: 8086
  user: no-need
tags:
  host: testhost.de
  region: europe
port: "/dev/ttyUSB*"
inverter_ids: [1,2,3]
read_interval_seconds: 10
...
[not up to date, check config.yaml as example]
```

run logger in folder where `config.yaml` is located
```
kaco_logger
```

## SMA Sunny Boy over RS485

TODO

## SMA Sunny Mini Central over Bluetooth

TODO

## Additional Statistics
- uptime (TODO)
- last request status
- reboot reason (TODO)
- awk '/MemFree/{print $2}' /proc/meminfo (TODO)

## Watchdog Manager

Implemenetd in all loggers, some minor differences.

#### Registered Checks:
- no internet for some amount of time
- no port (ttyUSB) found for some amount of time

#### Check for Reboot:
- check need for reboot
    - regularly check a function or result set by user
    - register function to check and how often it has to fail in a row
- check if uptime enough
- log reboot reason
- reboot


## TODO
- deploy using some software, e.g.
http://stackoverflow.com/questions/32830428/where-should-i-be-organizing-host-specific-files-templates

- make distributio of raspberry reliable and always-on
https://k3a.me/how-to-make-raspberrypi-truly-read-only-reliable-and-trouble-free/
https://wiki.debian.org/ReadonlyRoot
https://info-beamer.com/blog/building-a-reliable-raspberry-pi-distribution
http://www.sixteen-nine.net/2016/05/18/screenlys-raspberry-pi-powered-platform-shifting-to-new-iot-version-of-ubuntu-linux/


- update system time before we use it in the app (otherwise time changes too often
and we will reboot without reason...)
- see sudo ntpd -q -g and http://raspberrypi.stackexchange.com/questions/8231/how-to-force-ntpd-to-update-date-time-after-boot

