def custom_index(active,position):
    if page[active][position][3][3][0] == 'mqtt':
        return mqtt(page[active][position][3][0],page[active][position][3][3][1],page[active][position][3][3][2])

def mqtt(mqtt_command,mqtt_type,mqtt_recherche):
    returncommand = subprocess.check_output(mqtt_command, shell = True )
    returncommand = returncommand.decode(encoding)
    off = returncommand.find(mqtt_recherche)
    if mqtt_type == "prise":
        if returncommand[off+11] == "O" and returncommand[off+12] == "N":
            return "1"
        elif returncommand[off+11] == "O" and returncommand[off+12] == "F":
            return "0"
        else:
            return "inconnue"
    elif mqtt_type == "temp" or mqtt_type == "humi":
        if mqtt_type == "temp":
            off += 13
        elif mqtt_type == "humi":
            off += 10
        temp = ""
        for a in range(15):
            if returncommand[off+a] == ",":
                break
            temp += returncommand[off+a]
        if mqtt_type == "temp":
            temp += "°C"
        elif mqtt_type == "humi":
            temp += " %"
        return temp
