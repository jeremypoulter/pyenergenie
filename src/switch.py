import time
import energenie
import paho.mqtt.client as mqtt

def setup_tool():
    device = energenie.registry.get("fish tank")
    #device = energenie.Devices.MIHO008((0x24780, 1))
    device.turn_on()


# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("alexa/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))
    name = msg.topic.split("/", 2)[1]
    device = energenie.registry.get(name)
    if str(msg.payload) == "1":
        print(name+" on")
        device.turn_on()
    else:
        print(name+" off")
        device.turn_off()


def main():
    energenie.init()
    while True:
        try:
            client = mqtt.Client()
            client.on_connect = on_connect
            client.on_message = on_message

            client.username_pw_set("emonpi", "emonpimqtt2016")
            client.connect("home.lan", 1883, 60)

            # Blocking call that processes network traffic, dispatches callbacks and
            # handles reconnecting.
            # Other loop*() functions are available that give a threaded interface and a
            # manual interface.
            client.loop_forever()
        finally:
            energenie.finished()

if __name__ == "__main__":
    main()