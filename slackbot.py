import time
import re
from slackclient import SlackClient
from threading import Thread
from Constants import *
import json
import FLib


# initantiate Slack client
slack_client = SlackClient('###,###,###')
# starterbot's user ID in Slack: value is assigned after the bot starts up
starterbot_id = None


# Functions ------------------------------
def bot_talks(message, default_message, Channel):
    slack_client.api_call(
        method="chat.postMessage",
        channel=Channel,
        text=message['text'] or default_message,
        attachments=json.dumps(message['attachments'])
    )


def parse_direct_mention(message_text):
    matches = re.search(MENTION_REGEX, message_text)
    return (matches.group(1), matches.group(2).strip()) if matches else (None, None)


def parse_bot_commands(slack_events):
    for event in slack_events:
        if event["type"] == "message" and not  "subtype" in event:
            user_id, message = parse_direct_mention(event["text"])
            if user_id == starterbot_id:
                return message, event["channel"]
    return None, None


def handle_command(command, channel):
    default_response = None
    response = None
    # Help commands
    if command.startswith("Hi"):
        response = "Hello"
    if command.startswith(HELP_COMMAND):
        words = command.split()
        if len(words) == 2:
            if words[1] == "Build":
                response = HELP_BUILD
            if words[1] == "Set":
                response = HELP_SET
            if words[1] == "Check":
                response = HELP_CHECK
            else:
                response = HELP_INFO
        else:
            response = HELP_INFO
    # Build commands
    if command.startswith(BUILD_COMMAND):
        words = command.split()
        if len(words) == 2:
            if words[1] == "Start":
                response = FLib.BUILD_START()
            if words[1] == "Stop":
                response = FLib.BUILD_STOP()
                FLib.BUILD_STOP()
            if words[1] == "Pause":
                response = FLib.Sform("Pausing Build...")
                FLib.BUILD_PAUSE()
            if words[1] == "Status":
                response = FLib.JOB_INFO("#Job Name")
            if words[1] == "Output":
                response = FLib.GET_OUTPUT("Job Name", #Build Number#)
            else:
                resp = "Please Specify what to do... Type 'Help Build' for help"

        else:
            resp = "Please Specify what to do... Type 'Help Build' for help"
            response = FLib.Sform(resp)
    # Set command
    if command.startswith(SET_COMMAND):
        words = command.split()
        if len(words) == 2:
            BUILD_TIME = "Next Build Run Re-programmed at: %s" % words[1]
            response = FLib.Sform(BUILD_TIME)
            FLib.BUILD_SET(BUILD_TIME)
        else:
            response = "Please Specify the time in the {hrs:mins:sec} format..."
    # Check command
    if(command == "Check"):
        BUILD_TIME = "Next Build Run Programmed at: %s" % FLib.CHECK_TIME()
        response = FLib.Sform(BUILD_TIME)
    if(command == "Info"):
        Version = "The Current Version running on Jenkins is %s" % FLib.GET_VER()
        response = FLib.Sform(Version)
    else:
        default_response = "Not sure what you mean. Try *{}*.".format(HELP_COMMAND)
    bot_talks(response, default_response, channel)

# Main Function ----------------------------------


def Comunication_LOOP():
    while True:
        command, channel = parse_bot_commands(slack_client.rtm_read())
        if command:
            handle_command(command, channel)
        time.sleep(RTM_READ_DELAY)


def Notification_LOOP():
    while True:
        if FLib.CHECK_RUN(FLib.server.get_running_builds()):
            num = FLib.GET_RUNNING_NUM()
            i = 0
            More_output = True
            bot_talks(FLib.MESSAGE_START(num), None, FLib.Slack_Channel)
            output = FLib.server.get_build_console_output("Job Name", num)
            while FLib.CHECK_RUN(FLib.server.get_running_builds()) or More_output:
                joutput = output.splitlines()
                print("%i \n %i" % (len(joutput), i))
                if len(joutput) > i:
                    bot_talks(FLib.Serialform(joutput[i]), None, FLib.Slack_Channel)
                    if (joutput[-1].startswith("Finished:") and (joutput[-1] == joutput[i])):
                            More_output = False
                    i += 1
                else:
                    time.sleep(10)
                    output = FLib.server.get_build_console_output("Job Name", num)
            bot_talks(FLib.MESSAGE_END(num), None, FLib.Slack_Channel)


if __name__ == "__main__":
    if slack_client.rtm_connect(with_team_state=False):
        print("Starter Bot connected and running!")
        bot_talks(Starter_Bot, None, FLib.Slack_Channel)
        # Read bot's user ID by calling Web API method `auth.test`
        starterbot_id = slack_client.api_call("auth.test")["user_id"]
        F1 = Thread(target=Comunication_LOOP)
        F2 = Thread(target=Notification_LOOP)
        F1.setDaemon(True)
        F2.setDaemon(True)
        F1.start()
        F2.start()
        while True:
            pass
    else:
        print("Connection failed. Exception traceback printed above.")
