from mycroft import MycroftSkill, intent_file_handler


class MqttAutomationController(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_file_handler('controller.automation.mqtt.intent')
    def handle_controller_automation_mqtt(self, message):
        self.speak_dialog('controller.automation.mqtt')


def create_skill():
    return MqttAutomationController()

