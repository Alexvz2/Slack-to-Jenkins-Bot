# -------Constants --------------------------------------------------------

slack_client = 'Slack CLient ID'

starterbot_id = None

Jenkins_adress = 'Jenkins Adress'

User_name = 'User Name'

Jenkins_Password = 'Password'

Jenkins_Job = "Job Name"

Slack_Channel = "Slack Channel To Post in"

Starter_Bot = {
    "text": None,
    "attachments": [
        {
            "fallback": "Required plain-text summary of the attachment.",
            "color": "#####",
            "title": "SlackBot Up and Running!!!",
            "text": "Type 'Help' for Help"
        }
    ]
}

# -------- Settings -------------------------------------------------------
RTM_READ_DELAY = 1  # 1 second delay between reading from RTM

MENTION_REGEX = "^<@(|[WU].+?)>(.*)"

# -------Commands ---------------------------------------------------------
BUILD_COMMAND = "Build"  # Build Start/Stop/Status

SET_COMMAND = "Set"  # Set's Build time

CHECK_COMMAND = "Check"  # Check Next Build time

INFO_COMMAND = "Info"  # return Jenkins Build Version

HELP_COMMAND = "Help"

HELP_INFO = {
    "text": "Help Menu",
    "attachments": [
        {
            "title": "Commands",
            "fields": [
                {
                    "title": "Build",
                    "value": "{Start/Stop/Pause/Status}",
                    "short": True
                },
                {
                    "title": "Set",
                    "value": "{time}",
                    "short": True
                },
                {
                    "title": "Check",
                    "value": "",
                    "short": True
                }
            ],
            "color": "#00BFFF"
        }
    ]
}

HELP_BUILD = {
    "text": "Build Help",
    "attachments": [
        {
            "title": "Build Commands",
            "fields": [
                {
                    "title": "Build Start",
                    "value": "Starts a Build of the Smoke Test",
                    "short": True
                },
                {
                    "title": "Build Stop",
                    "value": "Stops the Build of the Smoke Test",
                    "short": True
                },
				{
                    "title": "Build Pause",
                    "value": "Pauses the Cyclic Build Run",
                    "short": True
                },
                {
                    "title": "Build Continue",
                    "value": "Continues the Cyclic Build Run",
                    "short": True
                },
                {
                    "title": "Build Status ",
                    "value": "Returns the current status of the build(success:failure)",
                    "short": True},
                {
                    "title": "Build Output",
                    "value": "Prints the last build Output",
                    "short": True}
            ],
            "color": "#00BFFF"}
    ]
}

HELP_SET = {
    "text": "Help Set",
    "attachments": [
        {
            "title": "Set Commands",
            "fields": [
                {
                    "title": "Set {Time}",
                    "value": "Sets an autonomous build run in the {hrs:min:sec} format",
                }
            ],
            "color": "#00BFFF"
        }
    ]
}

HELP_CHECK = {
    "text": "Help Check",
    "attachments": [
        {
            "title": "Check Command",
            "fields": [
                {
                    "title": "Check",
                    "value": "Returns the time until the next build starts {hrs:min:sec}"
                }
            ],
            "color": "#00BFFF"
        }
    ]
}
