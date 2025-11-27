import paho.mqtt.client as mqtt
import time


class MQTT:
    def __init__(self, nome_client, subscriber= False):
        self.client = mqtt.Client(nome_client, subsciber)			#True per un subscriber, False per un publisher
        
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_subscibe = self.on_subscribe
        self.client.on_publish = self.on_publish
        self.client.on_message = self.on_message
        self.client.on_log = self.on_log
        
        self.connected_flag = False
        
    def start(self):
        print("\nConnessione...")
        self.client.connect("test.mosquitto.org", 1883, 60)
        self.client.loop_start()
        
        while not self.connected_flag:
            print("Attesa connessione...")
            time.sleep(0.1)
        
    def stop(self):
        self.client.loop_stop()
        self.client.disconnect()
        
        # Bisogna ggiungere un modo per controllare se il mio client è un subscriber ed effettuare self.clien.unsubscribe
        
        
    # The callback for when the client receives a
    # CONNACK response from the server.
    def on_connect(self, client, userdata, flags, rc):
        global loop_flag
        print("Connected with result code "+str(rc))
        print("\n connected with client "+ str(client))
        print("\n connected with userdata "+str(userdata))
        print("\n connected with flags "+str(flags))
        loop_flag=0
        
    def on_disconnect(self):
        print("\nDisconnected") #da modificare
        
    def on_subscribe(self, client, userdata, msg, qos_l):
        print("\non_sub: client ="+str(client))
        print("\non_sub: msg ="+str(msg))
        print("\non_sub: qos level ="+str(qos_l))
        
    def on_unsubscribe(self):
        print("\nUnsubscribed") #da modificare
        
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
        

        

