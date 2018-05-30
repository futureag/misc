# split image into multiple parts and send as multiple messages.
# Parts can be received in any order and reassembled when all are received.

import base64
import json
import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
#    print("Connected with result code "+str(rc))
    pass


def convertImageToBase64(img):
 with open(img, "rb") as image_file:
     encoded = base64.b64encode(image_file.read())
 return encoded

import random, string

def randomword(length):
 return ''.join(random.choice(string.lowercase) for i in range(length))

import math

packet_size=3000

def getFileName(pic):
    fn=pic.split("/")
    return fn[-1:][0]

def publishEncodedImage(encoded, pic):

 end = packet_size
 start = 0
 length = len(encoded)
 picId = randomword(8)
 pos = 0
 no_of_packets = math.ceil(length/packet_size)

 
 while start <= len(encoded):
     data = {"data": encoded[start:end], "pic_id":picId, "pos": pos, "size": no_of_packets, "file_name": getFileName(pic)}
     pubMQTT("Image-Data",json.JSONEncoder().encode(data))
     end += packet_size
     start += packet_size
     pos = pos +1

def pubMQTT(name, msg):
    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect("test.mosquitto.org", 1883, 60)
#    client.connect("iot.eclipse.org", 1883, 60)    
    topic='OpenAgBloom/' + name
    print "Topic: ", topic
    client.publish(topic, msg)
    client.disconnect()

def sendImg(pic):
    encoded=convertImageToBase64(pic)
    publishEncodedImage(encoded, pic)    
    
    

def test():
    pic="/home/pi/MVP/web/SmallImg.png"
    sendImg(pic)
#    print getFileName(pic)

     
if __name__=="__main__":
    test()

'''
 function reconstructBase64String(chunk) {
    pChunk = JSON.parse(chunk["d"]);

    //creates a new picture object if receiving a new picture, else adds incoming strings to an existing picture 
    if (pictures[pChunk["pic_id"]]==null) {
        pictures[pChunk["pic_id"]] = {"count":0, "total":pChunk["size"], pieces: {}, "pic_id": pChunk["pic_id"]};

        pictures[pChunk["pic_id"]].pieces[pChunk["pos"]] = pChunk["data"];

    }

    else {
        pictures[pChunk["pic_id"]].pieces[pChunk["pos"]] = pChunk["data"];
        pictures[pChunk["pic_id"]].count += 1;


        if (pictures[pChunk["pic_id"]].count == pictures[pChunk["pic_id"]].total) {
        console.log("Image reception compelete");
        var str_image=""; 

        for (var i = 0; i <= pictures[pChunk["pic_id"]].total; i++) 
            str_image = str_image + pictures[pChunk["pic_id"]].pieces[i];

        //displays image
        var source = 'data:image/jpeg;base64,'+str_image;
        var myImageElement = document.getElementById("picture_to_show");
        myImageElement.href = source;
        }

    }

}
'''
