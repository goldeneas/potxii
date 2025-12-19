from umqttsimple import MQTTClient
import time
import machine

class MicroMQTT:
    def __init__(self, client_name, ssd1306):
        self.client_name = client_name
        self.display = ssd1306
        
        self.client = None
        self.connected_flag = False
        
        self.command_handler = None
        
        #Lista dei topic sottoscritti dal subscriber
        self.subscriptions = []
        
    def set_handler(self, handler_function):
        #Metodo per impostare la funzione da chiamare quando arriva un messaggio
        self.command_handler = handler_function
        
    def connect(self, broker_ip, broker_port, user, password):
        
        self.broker_ip = broker_ip 
        self.port = broker_port
        self.user = user    
        self.password = password
        
        #Client MQTT
        self.client = MQTTClient(self.client_name, self.broker_ip, self.port, self.user, self.password)
        
        #Callback dei metodi
        self.client.set_callback(self.sub_cb)
        
        self.display.fill(0) 
        self.display.text("Connessione a:", 0, 0)
        self.display.text(self.broker_ip, 0, 10) 
        self.display.show()
        
        print("\nConnessione a " + self.broker_ip + "...")
        try:
            self.client.connect()
            self.connected_flag = True
            
            self.display.text("MQTT connesso", 0, 20)
            self.display.show()
            
            print("Connesso")
            
            for topic in self.subscriptions:
                self.client.subscribe(topic, 0)
            
        except OSError as e:
            self.display.fill(0)
            self.display.text("Errore Connessione:", 0, 0)
            self.display.text(str(e), 0, 15) 
            self.display.show()

            self.connected_flag = False
            print("Errore connessione: ", e)
            self.reconnect()

    def subscribe(self, topic):
    
        if not self.connected_flag:
            print("Impossibile iscriversi: Client non connesso")
            return

        try:
            self.client.subscribe(topic, 0)
            self.subscriptions.append(topic)
            
            self.display.fill(0)
            self.display.text("Iscritto a:", 0, 0) 
            self.display.text(topic, 0, 15)
            self.display.show()
            
            print("Iscritto al topic: " + topic)
        except OSError as e:
            print("Errore durante la sottoscrizione: ", e)
            
    def publish(self, topic, msg):
        if self.connected_flag:
            try:
                self.client.publish(topic, msg, False, 0)
            except OSError:
                print("Errore pubblicazione")
 
    def reconnect(self):
        self.display.fill(0)
        self.display.text("Riconnessione", 0, 0)
        self.display.show()
        
        print("Riconnessione")
        try:
            self.client.close() # Chiude la vecchia socket
        except:
            pass
        
        try:
            self.client.connect()
            self.connected_flag = True
            
            for topic in self.subscriptions:
                self.client.subscribe(topic, 0)
                
            print("Riconnesso con successo!")
            self.display.text("Riconnesso con successo!", 0, 10)
            self.display.show()
            
        except OSError as e:
            print("Riconnessione fallita:", e)
            self.display.text("Riconnessione fallita", 0, 10)
            self.display.show()
            self.connected_flag = False
        
    def sub_cb(self, topic, msg):
        topic_str = topic.decode("utf-8")
        msg_str = msg.decode("utf-8")
        
        if self.command_handler:
            print("DEBUG: Chiamo l'handler di MQTT")
            self.command_handler(topic_str, msg_str)

    def check_msg(self):
        if not self.connected_flag:
            print("Hai provato a chiamare check_msg, ma non siamo connessi!")

        print("Controllo se ho ricevuto messaggi...")

        try:
            self.client.check_msg()
        except OSError:
            self.connected_flag = False
            self.reconnect()   

