import paho.mqtt.client as mqtt
import time


class PC_MQTT:
    #clean_session determina come il broker gestisce lo stato del client tra una connessione e l’altra.
    #True => NON conserva lo stato del client
    #False => Mantiene lo stato del client
    def __init__(self, name, clean_session= False):
        self.name = name
        
        #Client MQTT
        self.client = mqtt.Client(name, clean_session)
        
        #Callback dei metodi
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_subscribe = self.on_subscribe
        self.client.on_publish = self.on_publish
        self.client.on_message = self.on_message
        self.client.on_log = self.on_log
        
        #Lista dei topic sottoscritti dal subscriber
        self.subscriptions = []
        
        self.loop_flag = False
        
    def start(self):
        print("\nConnessione...")
        self.client.connect("test.mosquitto.org", 1883, 60)
        self.client.loop_start()
        
        while not self.loop_flag:
            print("Attesa connessione...")
            time.sleep(0.1)
        
    def stop(self):
        #Entro nel for solo ho chiamato almeno una volta subscribe
        for topic in self.subscriptions:
            self.client.unsubscribed(topic)
        
        self.client.loop_stop()
        self.client.disconnect()
        
    #Operazioni di MQTT
    def subscribe(self, topic, qos=0):
        self.subscriptions.append(topic)
        return self.client.subscribe(topic, qos)

    def publish(self, topic, message, qos=0):
        return self.client.publish(topic, message, qos)
    
    #Callbacks
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))
        print("\n connected with client "+ str(client))
        print("\n connected with userdata "+str(userdata))
        print("\n connected with flags "+str(flags))
        self.loop_flag= True
        
    def on_disconnect(self, client, userdata, rc):
        print("\nDisconnected")			#da modificare
        
    def on_subscribe(self, client, userdata, msg, qos_l):
        print("\non_sub: client ="+str(client))
        print("\non_sub: msg ="+str(msg))
        print("\non_sub: qos level ="+str(qos_l))
        
    def on_unsubscribe(self, client, userdata, mid):
        print("\nDisconnected")			#da modificare
        
    def on_publish(self, client,userdata,result): #create function for callback
        print("data published \n")
        print("client = "+ str(client))
        print("\nresult in on_publish= ", result)

    # The callback for when a PUBLISH message is received from the server.
    def on_message(self, client, userdata, msg):
        print("\n on message: "+msg.topic+" "+str(msg.payload))
        
    def on_log(self, client, userdata, level, buf):
        print("\n log:client = "+ str(client))
        print("\n log:level ="+str(level))
        print("\n log:buffer "+str(buf))