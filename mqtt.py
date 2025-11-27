import paho.mqtt.client as mqtt
import time

# The callback for when the client receives a
# CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    global loop_flag
    print("Connected with result code "+str(rc))
    print("\n connected with client "+ str(client))
    print("\n connected with userdata "+str(userdata))
    print("\n connected with flags "+str(flags))
    loop_flag=0
    
def on_disconnect():
    print("\nDisconnected") #da modificare
    
def on_subscribe(client, userdata, msg, qos_l):
    print("\non_sub: client ="+str(client))
    print("\non_sub: msg ="+str(msg))
    print("\non_sub: qos level ="+str(qos_l))
    
def on_unsubscribe():
    print("\nUnsubscribed") #da modificare
    
def on_publish(client,userdata,result): #create function for callback
    print("data published \n")
    print("client = "+ str(client))
    print("\nresult in on_publish= ", result)

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print("\n on message: "+msg.topic+" "+str(msg.payload))
    
def on_log(client, userdata, level, buf):
    print("\n log:client = "+ str(client))
    print("\n log:level ="+str(level))
    print("\n log:buffer "+str(buf))
    

    
