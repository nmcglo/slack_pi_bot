import os
from subprocess import call
from slackclient import SlackClient
from time import sleep
from PIL import Image


token = os.environ.get('SLACK_BOT_TOKEN')
botid = os.environ.get('SLACK_BOT_ID')



AT_BOT = "<@" + botid + ">:"

#commands
timecommand = 'time'
screencap = 'screencap'
picam = 'picam_12345'

sc = SlackClient(token)


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None

def handle_command(command, channel):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = "Not sure what you mean. Use the *"+"* command with numbers, delimited by spaces."
    if command.startswith(timecommand):
        timecommandfun()
    elif command.startswith(screencap):
        screencapcommandfun()
    elif command.startswith(picam):
        rpicamcommandfun()
    else:
        response = "Na-ah-ah, you didn't say the magic word!"
        sc.api_call("chat.postMessage", channel=channel, text=response, as_user=True)
        print("Failed command")


def rpicamcommandfun():
    call(['sudo', 'raspistill', '-awb', 'auto', '-co', '20', '-o', 'image.jpg'])

    test_image = "image.jpg"
    original = Image.open(test_image)
    # original.show()

    width, height = original.size   # Get dimensions
    left = 0
    top = int(height/2)
    right = width
    bottom = height
    cropped_example = original.crop((left, top, right, bottom))

    cropped_example.save('image.jpg','JPEG')

    FNULL = open(os.devnull, 'w')
    call(["curl", "-F", "file=@image.jpg", "-F", "channels="+channel,  "-F", "token="+token, "https://slack.com/api/files.upload"],stdout=FNULL)
    print("Someone accessed the camera!")

def screencapcommandfun():
    response = "Sorry, the Raspberry Pi has no screen to capture!"
    sc.api_call("chat.postMessage", channel=channel, text=response, as_user=True)
    print("Someone tried to screencap")

    # call(["screencapture", "test.jpg"])
    #
    # im = Image.open("test.jpg")
    # # print(im.format, im.size, im.mode)
    #
    # test_image = "test.jpg"
    # original = Image.open(test_image)
    # # original.show()
    #
    # width, height = original.size   # Get dimensions
    # left = 12 * width/14
    # top = 0
    # right = width
    # bottom = height/20
    # cropped_example = original.crop((left, top, right, bottom))
    #
    # cropped_example.save("test.jpg", "JPEG")
    #
    # call(["curl", "-F", "file=@test.jpg", "-F", "channels="+channel,  "-F", "token="+token, "https://slack.com/api/files.upload"])
    # # print(sc.api_call("files.upload", file="test.jpg", filename="tempscreengrab", channels=channel))
    # print("someone executed a screengrab!")



def timecommandfun():
    response = "The current time at Neil's Raspberry Pi is:\n"
    f = os.popen('date')
    now = f.read()
    response += now
    print("Someone polled the time")
    sc.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if sc.rtm_connect():
        print("StarterBot connected and running!")
        while True:
            command, channel = parse_slack_output(sc.rtm_read())
            if command and channel:
                handle_command(command, channel)
            sleep(READ_WEBSOCKET_DELAY)
    else:
        print("Connection failed. Invalid Slack token or bot ID?")
