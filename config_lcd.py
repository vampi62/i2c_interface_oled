# 1 = button, 2 = info, 3 = info+button
# format : ['texte',page si nav_ou_commande=True ,nav_ou_commande,['commande executer','affichage si 0','affichage si 1',['function custom','option1','option2']],['commande si button','option1 si info=1','option2 si info=0']]
p0 = []
p1 = []
p2 = []
p3 = []
p4 = []
page = []
nav = []

p0.append(['energie',1,True,['','','',['','','']],['','','']])
p0.append(['gestion',2,True,['','','',['','','']],['','','']])
p0.append(['resource',3,True,['','','',['','','']],['','','']])
p0.append(['temperature',4,True,['','','',['','','']],['','','']])

p1.append(['prise_1 :',3,False,['mosquitto_sub -h 192.168.5.1 -t zigbee2mqtt/labo_multiprise -u zigbee -P jee4mqt2sub -C 1','OFF','ON',['mqtt','prise','state_l1']],['mosquitto_pub -h 192.168.5.1 -t zigbee2mqtt/labo_multiprise/set -u zigbee -P jee4mqt2sub -m ','"{ \\"state_l1\\": \\"OFF\\" }\"','\"{ \\"state_l1\\": \\"ON\\" }\"']])
p1.append(['prise_2 :',3,False,['mosquitto_sub -h 192.168.5.1 -t zigbee2mqtt/labo_multiprise -u zigbee -P jee4mqt2sub -C 1','OFF','ON',['mqtt','prise','state_l2']],['mosquitto_pub -h 192.168.5.1 -t zigbee2mqtt/labo_multiprise/set -u zigbee -P jee4mqt2sub -m ','"{ \\"state_l2\\": \\"OFF\\" }\"','\"{ \\"state_l2\\": \\"ON\\" }\"']])
p1.append(['prise_3 :',3,False,['mosquitto_sub -h 192.168.5.1 -t zigbee2mqtt/labo_multiprise -u zigbee -P jee4mqt2sub -C 1','OFF','ON',['mqtt','prise','state_l3']],['mosquitto_pub -h 192.168.5.1 -t zigbee2mqtt/labo_multiprise/set -u zigbee -P jee4mqt2sub -m ','"{ \\"state_l3\\": \\"OFF\\" }\"','\"{ \\"state_l3\\": \\"ON\\" }\"']])
p1.append(['prise_4 :',3,False,['mosquitto_sub -h 192.168.5.1 -t zigbee2mqtt/labo_multiprise -u zigbee -P jee4mqt2sub -C 1','OFF','ON',['mqtt','prise','state_l4']],['mosquitto_pub -h 192.168.5.1 -t zigbee2mqtt/labo_multiprise/set -u zigbee -P jee4mqt2sub -m ','"{ \\"state_l4\\": \\"OFF\\" }\"','\"{ \\"state_l4\\": \\"ON\\" }\"']])
p1.append(['usb     :',3,False,['mosquitto_sub -h 192.168.5.1 -t zigbee2mqtt/labo_multiprise -u zigbee -P jee4mqt2sub -C 1','OFF','ON',['mqtt','prise','state_l5']],['mosquitto_pub -h 192.168.5.1 -t zigbee2mqtt/labo_multiprise/set -u zigbee -P jee4mqt2sub -m ','"{ \\"state_l5\\": \\"OFF\\" }\"','\"{ \\"state_l5\\": \\"ON\\" }\"']])

p2.append(['wifi driver',1,False,['','','',['','','']],['python restoredrive.py','','']])
p2.append(['fsck sd',1,False,['','','',['','','']],['python repare.py','','']])
p2.append(['ping gateway',1,False,['','','',['','','']],['python ping.py','','']])
p2.append(['redemarrage',1,False,['','','',['','','']],['python redemarrage.py','','']])
p2.append(['arret',1,False,['','','',['','','']],['python arret.py','','']])

p3.append(['IP   :',2,False,['hostname -I | cut -d\' \' -f1','','',['','','']],['','','']])
p3.append(['TEMP :',2,False,['vcgencmd measure_temp | cut -b 6-12','','',['','','']],['','','']])
p3.append(['CPU  :',2,False,["top -bn1 | grep load | awk '{printf \"%.2f%%\", $(NF-2)*10}'",'','',['','','']],['','','']])
p3.append(['RAM  :',2,False,["free -m | awk 'NR==2{printf \"%s/%sMB \", $3,$2 }'",'','',['','','']],['','','']])
p3.append(['DISK :',2,False,["df -h | grep 'root' | awk '{print $3 \"/\" $2 \" \" $5}'",'','',['','','']],['','','']])

p4.append(['TEMP :',2,False,['mosquitto_sub -h 192.168.5.1 -t zigbee2mqtt/labo_temp -u zigbee -P jee4mqt2sub -C 1','','',['mqtt','temp','temperature']],['','','']])
p4.append(['HUMI :',2,False,['mosquitto_sub -h 192.168.5.1 -t zigbee2mqtt/labo_temp -u zigbee -P jee4mqt2sub -C 1','','',['mqtt','humi','humidity']],['','','']])

page.append(p0)
nav.append("menu")
page.append(p1)
nav.append("menu/energie")
page.append(p2)
nav.append("menu/gestion")
page.append(p3)
nav.append("menu/resource")
page.append(p4)
nav.append("menu/temperature")