# pyhomebridge
python library to control a Homebridge server

## Setup
Install [homebridge-config-ui-x](https://www.npmjs.com/package/homebridge-config-ui-x) on your HomeBridge.

Make sure you run HomeBridge in Insecure Mode. (This can be changed in the Web Settings at top right corner)
API control is only allowed in this mode.
Thats starting HomeBridge with the -I flag.

## Installation
Pypi package for [pyhomebridge](https://pypi.org/project/pyhomebridge/)
```bash
pip3 install pyhomebridge
```

## Usage
Python usage:
```python
from homebridge import HomeBridgeController

controller = HomeBridgeController(host="homebridge.local", port=80, auth="123-45-678")
print(controller.accessories)
controller.print_accessories()
controller.accessory_exists("light_hallway")
controller.get_value("light_hallway")
controller.set_value("light_hallway", True)
```

In the repo you can find a python script to use for CLI execution. `control-homebridge.py`
```bash
python3 control-homebridge.py --list
python3 control-homebridge.py --name light_hallway --off

# you will need to set url, port and code in the script
# or use the --server, --port, --auth options
```

## Development

Currently supported devices:

* Lights
* Switches
* Outlets

## TODO

* add timeouts
* support more device types
* write documentation
* write tests
* much much more

## Inspiration
[HomeScript by menahishayan](https://github.com/menahishayan/HomeScript)

## License
[MIT](LICENSE)

**Free Software, Hell Yeah!**
