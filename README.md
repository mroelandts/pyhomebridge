# pyhomebridge
python library to control a Homebridge server

## Setup
Install [homebridge-config-ui-x](https://www.npmjs.com/package/homebridge-config-ui-x) on your HomeBridge.

Make sure you run HomeBridge in Insecure Mode. (This can be changed in the Web Settings at top right corner)
API control is only allowed in this mode.
Thats starting HomeBridge with the -I flag.

## Installation
```bash
# not yet
```

## Usage
```python
from homebridge import HomeBridgeController

controller = HomeBridgeController(host="homebridge.local", port=80, auth="123-45-678")
controller.print_accessories()
```

## Development

Currently supported devices:

* Lights
* Switches

## TODO

* add timeouts
* support more device types
* write documentation
* write tests
* much much more

## Inspiration
[HomeScript by menahishayan](https://github.com/menahishayan/HomeScript)

## License
----

MIT

**Free Software, Hell Yeah!**
