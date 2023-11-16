# Automation for Optical & Radio Astronomy Observatories

This repository is designed for deployment at an observatory site, where it receives tasking requests via REST to collect
optical and/or RF observations on various targets (deep sky objects, solar system objects, or satellites).

### Tasking
Tasking for the observatory is done using a REST API and the format provided by the `sensor_tasking` submodule.

### Sensors
Currently, only abstract base classes for optical and RF sensors are implemented. Derived classes enabling the
use of specific instruments are in-work.

### Automatic limit checking & alerts
The `limits` module contains classes to store sensor limits and check them against tasking requests to ensure a request
does not violate the system limits or request a collection type that the observatory cannot meet.

### Access calculations
Since tasking requests contain only target information- not specific commands for when/where to point a sensor, access
calculations must be performed at the observatory. The `lenoir` submodule provides the physics backend for this.