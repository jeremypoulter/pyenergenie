import time
import energenie
import paho.mqtt.client as mqtt
import Queue
import threading

q = Queue.Queue()

def controller():
    energenie.init()

    while True:
        try:
            msg = q.get()
            print(msg.topic+" "+str(msg.payload))
            name = msg.topic.split("/", 2)[1]
            device = energenie.registry.get(name)
            if str(msg.payload) == "1":
                print(name+" on")
                for x in range(0, 5):
                    device.turn_on()
                    time.sleep(0.1)
            else:
                print(name+" off")
                for x in range(0, 5):
                    device.turn_off()
                    time.sleep(0.1)
        except:
            print("Got exception")
        finally:
            q.task_done()

# The callback for when the client receives a CONNACK response from the server.
def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("alexa/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    q.put(msg)

def main():
    # Start a thread to process the key presses
    t = threading.Thread(target=controller)
    t.daemon = True
    t.start()

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
            print("Restarting...")

if __name__ == "__main__":
    main()
