# 1 = button, 2 = info, 3 = info+button
# format : ['texte',page si nav_ou_commande=True ,nav_ou_commande,['commande executer','affichage si 0','affichage si 1',['function custom','option1','option2']],['commande si button','option1 si info=1','option2 si info=0']]
p0 = []
p1 = []
p2 = []
p3 = []
p4 = []
page = []
nav = []

p0.append({'txt':'energie','destinationPage':1})
p0.append({'txt':'gestion','destinationPage':2})
p0.append({'txt':'resource','destinationPage':3})
p0.append({'txt':'temperature','destinationPage':4})

p1.append({'txt':'prise_1 :','infoCommande':{'commande':'mosquitto_sub -h 192.168.5.1 -t zigbee2mqtt/labo_multiprise -u zigbee -P jee4mqt2sub -C 1','tag':'state_l1','type':'json'},'actionCommande':{'commande':'mosquitto_pub -h 192.168.5.1 -t zigbee2mqtt/labo_multiprise/set -u zigbee -P jee4mqt2sub -m ','ifResult':[['OFF', '"{ \\"state_l1\\": \\"ON\\" }\"'],['ON', '"{ \\"state_l1\\": \\"OFF\\" }\"']]}})
p1.append({'txt':'prise_2 :','infoCommande':{'commande':'mosquitto_sub -h 192.168.5.1 -t zigbee2mqtt/labo_multiprise -u zigbee -P jee4mqt2sub -C 1','tag':'state_l2','type':'json'},'actionCommande':{'commande':'mosquitto_pub -h 192.168.5.1 -t zigbee2mqtt/labo_multiprise/set -u zigbee -P jee4mqt2sub -m ','ifResult':[['OFF', '"{ \\"state_l2\\": \\"ON\\" }\"'],['ON', '"{ \\"state_l2\\": \\"OFF\\" }\"']]}})
p1.append({'txt':'prise_3 :','infoCommande':{'commande':'mosquitto_sub -h 192.168.5.1 -t zigbee2mqtt/labo_multiprise -u zigbee -P jee4mqt2sub -C 1','tag':'state_l3','type':'json'},'actionCommande':{'commande':'mosquitto_pub -h 192.168.5.1 -t zigbee2mqtt/labo_multiprise/set -u zigbee -P jee4mqt2sub -m ','ifResult':[['OFF', '"{ \\"state_l3\\": \\"ON\\" }\"'],['ON', '"{ \\"state_l3\\": \\"OFF\\" }\"']]}})
p1.append({'txt':'prise_4 :','infoCommande':{'commande':'mosquitto_sub -h 192.168.5.1 -t zigbee2mqtt/labo_multiprise -u zigbee -P jee4mqt2sub -C 1','tag':'state_l4','type':'json'},'actionCommande':{'commande':'mosquitto_pub -h 192.168.5.1 -t zigbee2mqtt/labo_multiprise/set -u zigbee -P jee4mqt2sub -m ','ifResult':[['OFF', '"{ \\"state_l4\\": \\"ON\\" }\"'],['ON', '"{ \\"state_l4\\": \\"OFF\\" }\"']]}})
p1.append({'txt':'usb     :','infoCommande':{'commande':'mosquitto_sub -h 192.168.5.1 -t zigbee2mqtt/labo_multiprise -u zigbee -P jee4mqt2sub -C 1','tag':'state_l5','type':'json'},'actionCommande':{'commande':'mosquitto_pub -h 192.168.5.1 -t zigbee2mqtt/labo_multiprise/set -u zigbee -P jee4mqt2sub -m ','ifResult':[['OFF', '"{ \\"state_l5\\": \\"ON\\" }\"'],['ON', '"{ \\"state_l5\\": \\"OFF\\" }\"']]}})

p2.append({'txt':'wifi driver','actionCommande':{'commande':'python restoredrive.py'}})
p2.append({'txt':'fsck sd','actionCommande':{'commande':'python repare.py'}})
p2.append({'txt':'ping gateway','actionCommande':{'commande':'python ping.py'}})
p2.append({'txt':'redemarrage','actionCommande':{'commande':'python redemarrage.py'}})
p2.append({'txt':'arret','actionCommande':{'commande':'python arret.py'}})

p3.append({'txt':'IP   :','infoCommande':{'commande':'hostname -I | cut -d\' \' -f1'}})
p3.append({'txt':'TEMP :','infoCommande':{'commande':'vcgencmd measure_temp | cut -b 6-12'}})
p3.append({'txt':'CPU  :','infoCommande':{"commande":"top -bn1 | grep load | awk '{printf \"%.2f%%\", $(NF-2)*10}'"}})
p3.append({'txt':'RAM  :','infoCommande':{'commande':"free -m | awk 'NR==2{printf \"%s/%sMB \", $3,$2 }'"}})
p3.append({'txt':'DISK :','infoCommande':{'commande':"df -h | grep 'root' | awk '{print $3 \"/\" $2 \" \" $5}'"}})

p4.append({'txt':'TEMP :','infoCommande':{'commande':'mosquitto_sub -h 192.168.5.1 -t zigbee2mqtt/labo_temp -u zigbee -P jee4mqt2sub -C 1','tag':'temperature','suffixe':' °C','type':'json'}})
p4.append({'txt':'HUMI :','infoCommande':{'commande':'mosquitto_sub -h 192.168.5.1 -t zigbee2mqtt/labo_temp -u zigbee -P jee4mqt2sub -C 1','tag':'humidity','suffixe':' %','type':'json'}})
p4.append({'txt':'FUME :','infoCommande':{'commande':'mosquitto_sub -h 192.168.5.1 -t zigbee2mqtt/labo_fumer -u zigbee -P jee4mqt2sub -C 1','tag':'smoke_density','suffixe':' ppm','type':'json'}})

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