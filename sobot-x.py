#!/usr/bin/env python3

# This script will automate Sonos controls through email
# By Robert John P. Canare
# Oct 24, 2020

# Time and SOCO module
from time import sleep
from datetime import datetime
from soco import SoCo

# Email module
import imaplib
import email

# Email credentials
username = "sonos@gmail.com"
password = "password"

# Email subjects into list
email_subjects = []

# Sonos information
my_zone = SoCo("172.16.8.10")

# Time information
now = str(datetime.now().time())
current_time = now[0:5]

# Sonos commands
list_of_commands = ["play christmas", "play mellow"]


# Read email subject function
def read_email():
    # create an IMAP4 class with SSL
    mail = imaplib.IMAP4_SSL("imap.gmail.com")
    # authenticate
    mail.login(username, password)
    mail.select()

    type, data = mail.search(None, 'ALL')
    for num in data[0].split():
        typ, data = mail.fetch(num, '(RFC822)')
        for response_part in data:
            if isinstance(response_part, tuple):
                msg = email.message_from_string(response_part[1].decode('utf-8'))
                email_subject = msg['subject']
                email_subjects.append(email_subject)

    latest_email = str.lower(email_subjects[-1])
    latest_email_1 = str.lower(email_subjects[-2])

    return [latest_email_1, latest_email]


from_email_subs = read_email()


# Extracting the command on the from_email_subs[1]
def extracting_command():
    command_string = str(from_email_subs[-1])

    sonos_validation = command_string.split()[0]
    sonos_command = command_string.split()[1]
    sonos_value = command_string.split()[2]

    return sonos_validation, sonos_command, sonos_value


sonos_validation = extracting_command()[0]
sonos_command = extracting_command()[1]
sonos_value = extracting_command()[2]


# Check if it's a Sonos command
def validate_sonos_command():
    cmd = f"{sonos_command} {sonos_value}"
    if sonos_validation == "sonos" and cmd in list_of_commands:
        return True, cmd
    else:
        return False


cmd = validate_sonos_command()


# Read executed_command.txt file and check if it's executed already
def check_executed_command():
    f = open("executed_command.txt", "r")
    executed_command = f.readline()
    if cmd == executed_command:
        file = open("executed_command.txt", "w")
        file.writelines(cmd)
        file.close()
        return False
    else:
        return


# Fading out the volume and clearing queue function
def fading_out():
    # Volume fade out
    my_zone.volume -= 5
    sleep(2)
    my_zone.volume -= 5
    sleep(2)
    my_zone.volume -= 5
    sleep(2)
    my_zone.volume -= 5
    sleep(2)
    my_zone.volume -= 5
    sleep(2)
    my_zone.volume -= 4
    sleep(2)
    # Clearing the queue
    my_zone.clear_queue()
    my_zone.volume += 5
    sleep(2)
    my_zone.volume += 5
    sleep(2)
    my_zone.volume += 5
    sleep(2)
    my_zone.volume = 40


# Play Christmas playlist function
def play_christmas():
    fading_out()
    play_list = my_zone.get_sonos_playlists()[8]  # <--- Christmas playlist number here
    my_zone.add_to_queue(play_list)
    my_zone.play()


# Play English oldies playlist function
def play_english_oldies():
    fading_out()
    play_list_1 = my_zone.get_sonos_playlists()[1]  # <--- English oldies playlist number here
    my_zone.add_to_queue(play_list_1)
    my_zone.play()


# Endless loop
while True:
    if validate_sonos_command() and check_list_of_commands() and check_if_its_executed():
        if sonos_value == "christmas":
            play_christmas()
        elif sonos_value == "mellow":
            play_english_oldies()
