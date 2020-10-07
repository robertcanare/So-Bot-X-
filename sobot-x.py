#!/usr/bin/env python3

################################################################################
# ______      _               _     _____            ______       _    __   __ #
# | ___ \    | |             | |   /  ___|           | ___ \     | |   \ \ / / #
# | |_/ /___ | |__   ___ _ __| |_  \ `--.  ___ ______| |_/ / ___ | |_   \ V /  #
# |    // _ \| '_ \ / _ \ '__| __|  `--. \/ _ \______| ___ \/ _ \| __|  /   \  #
# | |\ \ (_) | |_) |  __/ |  | |_  /\__/ / (_) |     | |_/ / (_) | |_  / /^\ \ #
# \_| \_\___/|_.__/ \___|_|   \__| \____/ \___/      \____/ \___/ \__| \/   \/ #
#                                                                              #
#                                                                              #
# _____                        ______       _                                  #
# /  ___|                       | ___ \     | |                                #
# \ `--.  ___  _ __   ___  ___  | |_/ / ___ | |_                               #
# `--. \/ _ \| '_ \ / _ \/ __| | ___ \/ _ \| __|                               #
# /\__/ / (_) | | | | (_) \__ \ | |_/ / (_) | |_                               #
# \____/ \___/|_| |_|\___/|___/ \____/ \___/ \__|                              #
################################################################################

# This script will automate Sonos control
# Sonos Bot Version X
# By Robert John P. Canare
# Oct 24, 2020

# Email instructions that Sonos can understand
# > sonos volume down
# > sonos volume up
# > sonos pause song
# > sonos play song
# > sonos play christmas
# > sonos play mellow

# Time and SOCO module
from time import sleep
from datetime import datetime
from soco import SoCo

# Email module
import imaplib
import email

# Email credentials
# account credentials
username = "sonos@gmail.com"
password = "pass"

# Email subjects into list
email_subjects = []

# Sonos information
my_zone = SoCo("172.16.8.10")
current_volume = my_zone.volume

# Time information
now = str(datetime.now().time())
current_time = now[0:5]

# Sonos commands
list_of_commands = ["volume down", "volume up", "pause song", "play song", "play christmas", "play mellow"]


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


# Get the latest 2 email subject
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
    if sonos_validation == "sonos":
        return True
    else:
        return False


cmd = f"{sonos_command} {sonos_value}"


# Check if the command is in the list of commands
def check_list_of_commands():
    if cmd in list_of_commands:
        return True
    else:
        return False


# Read executed_command.txt file and check if it's executed already
def check_executed_command():
    f = open("executed_command.txt", "r")
    executed_command = f.readline()
    return executed_command


executed = check_executed_command()


# Check if the recent command is executed already
def check_if_its_executed():
    if cmd == executed:
        return False
    else:
        return True


# update the first line of the executed_command.txt file
def replace_line(file_name, line_num, text):
    lines = open(file_name, 'r').readlines()
    lines[line_num] = text
    out = open(file_name, 'w')
    out.writelines(lines)
    out.close()


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


# Execution time function
def execution_time():
    # 6:00 AM play english oldies songs
    if current_time == "12:01":
        play_english_oldies()
    # 7:28 AM play christmas songs
    elif current_time == "12:00":
        play_christmas()
    else:
        print(current_time)


# <--------------- MAIN FUNCTION AND IT'S WORKING --------------->
# Executing the command from the latest email
def executing():
    if validate_sonos_command() and check_list_of_commands() and check_if_its_executed():
        print(f"Executing {cmd}")
        # Update the first the executed command on the executed_command.txt file
        print(f"Adding {cmd} to the executed")
        replace_line(f'executed_command.txt', 0, cmd)
    else:
        print("Do nothing")

# <------------------ WORK ON THIS PART ------------------>
# Create all the necessary function for Sonos, for example:
# volume_down()
# volume_up()
# pause_song()
# play_song()
