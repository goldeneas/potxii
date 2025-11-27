from umqtt.simple import MQTTClient
import time
import machine

class Micro_MQTT:
    def __init__(self, name_client):
        self.name_client = name_client
        
        #da modificare con il nostro server
        self.broker_ip = "test.mosquitto.org" 
        self.port = 1883
        self.user = None     
        self.password = None
        
        #Client MQTT
        self.client = MQTTClient(self.name, self.broker_ip, self.port, self.user, self.password)
        
        #Callback dei metodi
        self.client.set_callback(self.sub_cb)
        
        #Lista dei topic sottoscritti dal subscriber
        self.subscriptions = []
        
    def connect_and_subscribe(self, topic= None):
        print("\nConnessione a " + self.broker_ip + "...")
        try:
            self.client.connect()
            print("Connesso")
            
            if topic:
                self.client.subscribe(topic)
                self.subscriptions.append(topic)
                print("Iscritto a: " + topic)
                
        except OSError as e:
            print("Errore connessione: ", e)
            self.restart_and_reconnect()
        
    def restart_and_reconnect(self):
        print("\Riconnessione")
        time.sleep(10)
        machine.reset()
        
    def sub_cb(self, topic, msg):
        print((topic, msg))
    
    def check_msg(self):
        try:
            self.client.check_msg()
        except OSError:
            self.restart_and_reconnect()
    