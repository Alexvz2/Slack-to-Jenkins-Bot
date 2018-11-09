import jenkins
from slackclient import SlackClient
from Constants import *

slack_client = SlackClient('##############')

server = jenkins.Jenkins(Jenkins_adress,
                         username=User_name,
                         password=Jenkins_Password
                         )


def Sform(text):
    script = {"text": "", "attachments": [{"title": " %s" % text, "color": "#00BFFF"}]}
    return script


def Serialform(text):
    script = {"text": " %s" % text, "attachments": None}
    return script


# returns the version currently running on Jenkins
def GET_VER():
    useless = server.get_whoami()  # required to call in order to initiate get_version
    version = server.get_version()
    return version


def GET_RUNNING_NUM():
    Num = server.get_running_builds()[0]['number']
    return Num


def NEXT_BUILD():
    NBuild = server.get_job_info(Jenkins_Job)['nextBuildNumber']
    return NBuild


# Provides a more readable job info format
def JOB_INFO(name):
    info = server.get_job_info(name)
    healthreport = info['healthReport'][0]
    text = "{} \nScore: {}".format(healthreport['description'], healthreport['score'])
    return Sform(text)


def BUILD_START():
    server.build_job(Jenkins_Job, parameters=None, token=None)
    text = "Build Started"
    return Sform(text)


def BUILD_STOP():
    num = GET_RUNNING_NUM()
    server.stop_build(Jenkins_Job, num)
    text = "Build {} stopped".format(num)
    return Sform(text)


def BUILD_PAUSE():
    server.disable_job(Jenkins_Job)
    pass


def GET_OUTPUT(name, build_num):
    output = server.get_build_console_output(name, build_num)
    response = {
        "text": "Most Recent Output",
        "attachments": [
            {"color": "#C0C0C0", "text": "%s" % output}]
                }
    return response


def HumanTime(millis):
    millis = int(millis)
    seconds = (millis / 1000) % 60
    seconds = int(seconds)
    minutes = (millis / (1000*60)) % 60
    minutes = int(minutes)
    hours = (millis / (1000*60*60)) % 24
    time = "%d:%d:%d" % (hours, minutes, seconds)
    return time


def MESSAGE_START(num):
    Info = server.get_build_info(Jenkins_Job, num)
    name = Info['fullDisplayName']
    description = Info['actions'][0]['causes'][0]['shortDescription']
    estimate = HumanTime(Info['estimatedDuration'])
    message = {
        "text": "Initiating Build",
        "attachments": [
            {
                "title": "%s Initiated" % name,
                "text": "%s\nEstimated Time: %s" % (description, estimate),
                "color": "#00BFFF"
            }
            ]
            }
    return message


def MESSAGE_END(num):
    colour = "#008000"
    Info = server.get_build_info(Jenkins_Job, num)
    name = Info['fullDisplayName']
    result = Info['result']
    if result != "SUCCESS":
        colour = "#FF0000"
    duration = HumanTime(Info['duration'])
    message = {
        "text": "End",
        "attachments": [
            {
                "title": "%s Finished" % name,
                "text": "Result: %s\nTotal Time: %s" % (result, duration),
                "color": colour
            }
            ]
            }
    return message


def CHECK_RUN(info):
    if len(info) is not 0:
        for name in info:
            if name["name"] == Jenkins_Job:
                return True
            else:
                return False
    else:
        pass
