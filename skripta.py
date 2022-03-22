import requests
import brotli
import time
import paho.mqtt.client as mqtt
from bs4 import BeautifulSoup

MQTT_BROKER = "broker.hivemq.com"
MQTT_PORT = 1883
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_TOPIC_ROOT = "ugradbeni/aprljaca1/"


def on_connect(client, userdata, flags, rc):
    print("{0}: Connected with result code {1}".format(time.asctime(),str(rc)))

def on_message(client, userdata, msg):
    print("{0}: {1} - {2}".format(time.asctime(),msg.topic,str(msg.payload)))

mqttclient = mqtt.Client()
mqttclient.on_connect = on_connect
mqttclient.on_message = on_message
mqttclient.username_pw_set(MQTT_USER,MQTT_PASSWORD)

mqttclient.connect(MQTT_BROKER, MQTT_PORT, 60)


while(True):
    headers = {
        'authority': 'www.klix.ba',
        'method': 'GET',
        'path': '/rss',
        'scheme': 'https',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'accept-encoding': 'gzip, deflate, br',
        'accept-language': 'en-US,en;q=0.9',
        'sec-ch-ua': 'Not;A Brand";v="99", "Google Chrome";v="91", "Chromium";v="91"',
        'sec-ch-ua-mobile': '?0',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'none',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36'
    }
    klixrssXML = requests.get('https://www.klix.ba/rss', headers=headers)

    #Čitanje RSS XML 
    klixrss = BeautifulSoup(klixrssXML.text, features="html.parser")
    clanci = klixrss.rss.channel.findAll("item")

    novosti = []
    for clanak in clanci:
        naslov = str(clanak.title)
        naslov = naslov.replace("<title>", "")
        naslov = naslov.replace("</title>", "")
        novosti.append(naslov)
    novosti = str(novosti)
    novosti = novosti.replace("', '","|")
    novosti = novosti.replace("'", "")
    novosti = novosti.replace("[", "")
    novosti = novosti.replace("]", "")
    mqttclient.publish(MQTT_TOPIC_ROOT, novosti)   
    print(novosti)
    time.sleep(1)
    


    