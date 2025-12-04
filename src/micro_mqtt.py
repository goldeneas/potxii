from umqttsimple import MQTTClient
import time
import machine

class MicroMQTT:
    def __init__(self, client_name, broker_ip, broker_port, ssd1306):
        self.client_name = client_name
        self.display = ssd1306
        
        #da modificare con il nostro server
        self.broker_ip = broker_ip 
        self.port = broker_port
        self.user = None     
        self.password = None
        self.__is_connected = False
        
        #Client MQTT
        self.client = MQTTClient(self.client_name, self.broker_ip, self.port, self.user, self.password)
        
        #Callback dei metodi
        self.client.set_callback(self.sub_cb)
        
        #Lista dei topic sottoscritti dal subscriber
        self.subscriptions = []
        
    def connect_and_subscribe(self, topic= None):
        self.display.fill(0) 
        self.display.text("Connessione a:", 0, 0)
        self.display.text(self.broker_ip, 0, 10) 
        self.display.show()
        
        #Tutte le print sono stampe di test da eliminare
        print("\nConnessione a " + self.broker_ip + "...")
        try:
            self.client.connect()
            self.display.fill(0)
            self.display.text("MQTT connesso", 0, 0)
            self.display.show()

            self.__is_connected = True
            
            print("Connesso")
            
            if topic:
                self.client.subscribe(topic)
                self.subscriptions.append(topic)
                
                self.display.text("Iscritto a:", 0, 10) 
                self.display.text(topic, 0, 20)
                self.display.show()
                
                print("Iscritto al topic: " + topic)
                
        except OSError as e:
            self.display.fill(0)
            self.display.text("Errore Connessione:", 0, 0)
            self.display.text(str(e), 0, 15) 
            self.display.show()

            self.__is_connected = False
            
            print("Errore connessione: ", e)
            
            self.restart_and_reconnect()
        
    def restart_and_reconnect(self):
        self.display.fill(0)
        self.display.text("Riconnessione", 0, 0)
        self.display.show()
        
        print("\Riconnessione")
        time.sleep(10)
        machine.reset()
        
    def sub_cb(self, topic, msg):
        print((topic, msg))
        
        topic_str = topic.decode()
        msg_str = msg.decode()
        
        self.display.fill(0)             
        self.display.text("Topic:", 0, 0)
        self.display.text(topic_str, 0, 10)
        
        self.display.text("Msg:", 0, 20)
        self.display.text(msg_str, 0, 30)
        
        self.display.show()

    def is_connected(self):
        return self.__is_connected
    
    def check_msg(self):
        try:
            self.client.check_msg()
        except OSError:
            self.__is_connected = False
            self.restart_and_reconnect()
    
