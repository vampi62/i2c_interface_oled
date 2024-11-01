# i2c_interface_oled

## Description

This project provides an interface using an OLED screen and navigation buttons for a Raspberry Pi, leveraging only the I2C port for communication. The pages are configured in the `config_lcd.py` file, allowing easy customization. Create a new page or add a section by following the steps below.

## Installation

Clone the project to the `/opt/` directory:

```bash
cd /opt
git clone https://github.com/vampi62/i2c_interface_oled.git
sudo chmod 755 -R /opt/i2c_interface_oled
sudo chown root:root -R /opt/i2c_interface_oled
```

Run the installation script to set up the service:

```bash
sudo ./install_service.sh
```

If you ever need to uninstall the service, an `uninstall_service.sh` script is provided to remove it.

## Configuration Guide

### Adding a New Page

To create a new page, follow these steps:
in the `config_lcd.py` file:

1. **Define a new list for the page:** Create an empty list for the new page, for example, `pX = []`, where `X` is the page number.
2. **Add components to the page list:** Each component on the page is represented by a dictionary formatted as follows:

    ```python
    # Example component button for change page
    pX.append({
        'txt': 'prise_2 :',
        'destinationPage': 1
    })
    # example component button for display information
    pX.append({
        'txt': 'IP :',
        'infoCommande': {
            'commande': 'hostname -I | cut -d\' \' -f1'
        }
    })
    # example component button for execute command
    pX.append({
        'txt': 'Reboot',
        'actionCommande': {
            'commande': 'sudo reboot'
        }
    })
    # you can combine infoCommande and actionCommande for create a button with information and action for toggle the state
    # Example component button 
    pX.append({
        'txt': 'prise_1 :',
        'infoCommande': {
            'commande': 'mosquitto_sub -h 192.168.5.1 -t zigbee2mqtt/labo_multiprise -u zigbee -P jee4mqt2sub -C 1',
            'tag': 'state_l1',
            'type': 'json',
            'txtResultLiteral': [['1', 'ON'], ['0', 'OFF']],
            'suffixe': ' °C'
        },
        'actionCommande': {
            'commande': 'mosquitto_pub -h 192.168.5.1 -t zigbee2mqtt/labo_multiprise/set -u zigbee -P jee4mqt2sub -m ',
            'ifResult': [['OFF', '"{ \\"state_l1\\": \\"ON\\" }"'], ['ON', '"{ \\"state_l1\\": \\"OFF\\" }"']]
        }
    })
    ```

   Only the `"txt"` field is mandatory; other fields can be omitted if not required.

   - **`txt`**: Text displayed for the component.
   - **`destinationPage`**: Page number to navigate to when the component is clicked.
   - **`infoCommande`**: The command that retrieves data from the sensor.
     - **`commande`**: The command to execute (mandatory for `infoCommande`).
     - **`type`**: Type of data to process (only `'json'` is supported currently).
     - **`tag`**: Tag to search for in the JSON output (required if `type` is `'json'`).
     - **`txtResultLiteral`**: A list of lists mapping each possible result value to a display string. If no match is found, the raw command output will be displayed.
       - For instance, if the command returns 0 or 1, `txtResultLiteral = [['0', 'OFF'], ['1', 'ON']]` will display `OFF` for 0 and `ON` for 1.
     - **`suffixe`**: A suffix added to the retrieved value.
   - **`actionCommande`**: Command executed when the component is clicked.
     - **`commande`**: Command to execute (mandatory for `actionCommande`).
     - **`ifResult`**: A list of lists specifying values to compare with the `infoCommande` result. If `infoCommande` returns a value matching an item in `[0]`, the corresponding `[1]` command will be sent. If no match is found, the last command parameter in the list will be used.
       - Example: If `infoCommande` returns 0 or 1, set `ifResult = [['0', '"{ \\"state_l1\\": \\"ON\\" }"'], ['1', '"{ \\"state_l1\\": \\"OFF\\" }"']]` to send `"{ \\"state_l1\\": \\"ON\\" }"` when `infoCommande` returns 0, and `"{ \\"state_l1\\": \\"OFF\\" }"` when it returns 1.

3. **Add the new page to the page list**: Once `pX` is fully defined, add it to the main `page` list: `page.append(pX)`.
4. **Add navigation links**: Update the `nav` list with the new page’s name, using `nav.append("menu/Yname")`, where `Yname` is the page’s name.

To create a specific page, you can add a new list in the `custom` dictionary. For example, to create a ping page:
```python
custom['ping'] = [{},{}]
custom['ping'][0]['nav'] = " - message - "
custom['ping'][0]['txt'] = ["",""]
custom['ping'][0]['txt'][0] = "ping box"
custom['ping'][0]['txt'][1] = "en cours"
custom['ping'][0]['txt'][2] = "192.168.1.1"
custom['ping'][0]['command'] = {}
custom['ping'][0]['command']["cmd"] = "ping 192.168.1.1 -c 1 | grep loss | awk '{printf $4}'"
custom['ping'][0]['command']['cwd'] = "/home/pi"
custom['ping'][0]['command']["result"] = {"0":2,"1":1}
custom['ping'][0]['goto'] = 2
custom['ping'][1]['nav'] = " - message - "
custom['ping'][1]['txt'] = ["",""]
custom['ping'][1]['txt'][0] = "ping box"
custom['ping'][1]['txt'][1] = "ok"
custom['ping'][1]['wait'] = 3
custom['ping'][1]['exit'] = True
```
explain:
- `nav` : texte show on the top of the page
- `txt` : list of text show on the page (0 to 2) for each line
- `command` : command to execute for get the result
- `['command']['cwd']` is optional, if you want to change the directory before execute the command
- `result` : dictionnary for mapping the result of the command with the next page
- `goto` : page number to go if the result is not dictionnary or if you don't want to use the 'result' dictionnary
- `wait` : time to wait before go to the next page
- `exit` : if True, exit the custom page after the wait time !! must be present at the end of the list for return to the normal menu !!

## Hardware

This project requires the following hardware components:

- **1 PCB** (schematics available in resources)
- **1 3D-printed case** (STL file available in resources)
- **1 OLED Display** - I2C 128x64 Pixels, 0.96-inch, SSD1306 ([Available on Amazon as a 5-pack](https://www.amazon.fr/gp/product/B08FD643VZ/ref=ppx_yo_dt_b_search_asin_title?ie=UTF8&psc=1))
- **1 PCF8574T** ([Available on Amazon as a 5-pack](https://www.amazon.fr/5-pi%C3%A8ces-PCF8574T-PCF8574-SOP16/dp/B0BFX2DV8R/ref=sr_1_11?__mk_fr_FR=%C3%85M%C3%85%C5%BD%C3%95%C3%91&crid=37VWEWKKIXPDK&keywords=PCF8574T&qid=1669558592&qu=eyJxc2MiOiIyLjUyIiwicXNhIjoiMi4wNCIsInFzcCI6IjEuODQifQ%3D%3D&sprefix=pcf8574t%2Caps%2C56&sr=8-11))
- **6 1K Ohm SMD resistors**
- **4 SMT push buttons**
- **2 Dupont connectors, 4x1 pin**

## Resources

- **PCB Schematics**: [OshwLab PCB](https://oshwlab.com/vadidi62/pi_oled__display)
- **3D Case STL File**: [Thingiverse STL File](https://www.thingiverse.com/thing:5661212)
- **Compatible STL File**: [Thingiverse STL File](https://www.thingiverse.com/thing:4249203)
- **Python Script**: [GitHub Repository](https://github.com/vampi62/i2c_interface_oled)

## Example Display Images

![Management Interface](https://github.com/vampi62/i2c_interface_oled/assets/104321401/cf43119e-e68e-4253-b3ea-c2c7cc74781a)
![Menu Interface](https://github.com/vampi62/i2c_interface_oled/assets/104321401/4cc85f9a-1c58-44fa-a93d-17ebc9c95dcb)
![IP Display](https://github.com/vampi62/i2c_interface_oled/assets/104321401/e961bb2d-ff13-4272-8741-93fe7bb70591)