import paho.mqtt.client as mqtt
import io
import Image
import json
import base64

#from set40On import set40On
#from set40Off import set40Off

pictures={}
path="/home/pi/Desktop/"

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("OpenAgBloom/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
#    print type(msg.payload)
#    print len(msg.payload)
    print msg.topic
#    print(msg.topic+" "+str(msg.payload))
    if msg.topic == 'OpenAgBloom/pic':
        ba=io.BytesIO(msg.payload)
        image=Image.open(ba)
        image.save("/home/pi/Desktop/Pic.jpg")
    elif msg.topic == 'OpenAgBloom/chart':
        pass
        image=Image.open(io.BytesIO(msg.payload))
        image.save("/home/pi/Desktop/Chart.svg")
    elif msg.topic == 'OpenAgBloom/byte':
        ba=bytearray(msg.payload)
        st = list(ba)
#        print st
        print "Size: ", len(ba)
    elif msg.topic == 'OpenAgBloom/Image-Data':
        reconstructBase64String(msg.payload)        
    else:
        print msg.payload

def reconstructBase64String(chunk):

    pChunk = json.loads(chunk)
#    pChunk = jchunk["data"]
    print pChunk["pic_id"], pChunk["pos"], pChunk["size"]
    #creates a new picture object if receiving a new picture, else adds incoming strings to an existing picture 
    if pictures.get(pChunk["pic_id"])==None:
        pictures[pChunk["pic_id"]] = {"count":0, "total":pChunk["size"], "pieces": [], "pic_id": pChunk["pic_id"]}
        print pictures

        pictures[pChunk["pic_id"]]["pieces"].insert(int(pChunk["pos"]),pChunk["data"])
    else:
        pictures[pChunk["pic_id"]]["pieces"].insert(int(pChunk["pos"]),pChunk["data"])
        pictures[pChunk["pic_id"]]["count"] += 1

        # Check if have all pieces
        if pictures[pChunk["pic_id"]]["count"] == pChunk["size"]:
            print "Image reception compelete"
            str_image=""

            # Dump chunks to image
            for i in range(pictures[pChunk["pic_id"]]["count"]):
                str_image = str_image + pictures[pChunk["pic_id"]]["pieces"][i]
            with open(path+pChunk["file_name"], "wb") as fh:
                fh.write(base64.decodestring(str_image))

        

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

#client.connect("test.mosquitto.org", 1883, 60)
client.connect("iot.eclipse.org", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()
