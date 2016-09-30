import os
from subprocess import call
from slackclient import SlackClient
from time import sleep


call(['sudo raspistill', '-awb', 'auto', '-co', '20', '-o', 'image.jpg'])
