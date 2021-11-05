from mycroft import MycroftSkill, intent_file_handler
import paho.mqtt.client as mqtt #import the mqtt client

class MqttAutomationController(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.mqtt_broker_address = "192.168.0.102"
        self.client = mqtt.Client("mycroft_pool_pump_ctl")
        self.client.on_message = self.on_message
        self.client.on_connect = self.on_connect
        self.client.on_publish = self.on_publish
        self.client.on_subscribe = self.on_subscribe
        return

    @intent_file_handler('controller.automation.mqtt.intent')
    def handle_controller_automation_mqtt(self, message):
        pump_state =  message.data.get('state')
        self.connect()
        if pump_state == 'on':
            self.speak_dialog('controller.automation.mqtt.on')
            self.client.publish("cmnd/sonoff-pump/Power1","on")
        elif pump_state == 'off':
            self.speak_dialog('controller.automation.mqtt.off')
            self.client.publish("cmnd/sonoff-pump/Power1","off")
        elif pump_state == 'activate':
            self.speak_dialog('controller.automation.mqtt.on')
            self.client.publish("cmnd/sonoff-pump/Power1","on")
        elif pump_state == 'deactivate':
            self.speak_dialog('controller.automation.mqtt.off')
            self.client.publish("cmnd/sonoff-pump/Power1","off")
        else:
            self.speak_dialog('controller.automation.mqtt.confused')
        self.disconnect()
        return

    def on_message(self, client, user_data, message):
        self.mqtt_message=message.payload.decode("utf-8")
        print("message:",self.mqtt_message)
        self.queue.put(self.mqtt_message)
        if (int(float(self.mqtt_message))==23):
            print("taking a photo")

    def on_connect(self, client, obj, flags, rc):
        print("rc: "+str(rc))

    def on_publish(self, client, obj, mid):
        print("mid: ",+str(mid))

    def on_subscribe(self, client, obj, granted_qos):
        print("subscribed: "+str(mid)+" "+str(granted_qos))

    def connect(self):
        print("Connecting to MQTT broker")
        self.client.connect(self.mqtt_broker_address)
        self.client.loop_start()
#        for topic in self.mqtt_topics:
#            self.client.subscribe(topic)

    def disconnect(self):
        print("Disconnecting from MQTT broker")
        self.client.loop_stop()

def create_skill():
    return MqttAutomationController()

