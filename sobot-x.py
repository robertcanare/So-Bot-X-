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
password = "password"

# Email subjects into list
email_subjects = []

# Sonos information
my_zone = SoCo("172.16.8.10")
current_volume = my_zone.volume

# Time information
now = str(datetime.now().time())
current_time = now[0:5]



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


# Check the latest email if executed already function
def is_it_executed():
    # Check the last 2 if it's the same
    if from_email_subs[0] == from_email_subs[1]:
        return False
    else:
        return True


# Extracting the command on the from_email_subs[1]
# The format should be:
#        Sonos            volume               up/down
# {valid sonos command}     {request}       {something}
def extracting_command():
    command_string = str(from_email_subs[-1])

    sonos_validation = command_string.split()[0]
    sonos_command = command_string.split()[1]
    sonos_value = command_string.split()[2]

    return sonos_validation, sonos_command, sonos_value


sonos_validation = extracting_command()[0]
sonos_command = extracting_command()[1]
sonos_value = extracting_command()[2]


# Already executed command
executed_commands = []


#  Executing the command from the latest email
def executing():
    if is_it_executed():
        if sonos_validation == "sonos":
            # I need something that once it's executed it won't execute again
            # WHAT IF ONCE NA EXECUTE NA IUUPDATE NYA YUNG LIST into NULL NA LANG??
            if sonos_command == "volume":
                print("Execute volume function")
                # Tong part na to dapat once lang mag execute
            elif sonos_command == "pause":
                print("Execute pause function")
                # Tong part na to dapat once lang mag execute
            elif sonos_command == "play":
                print("Execute play function")
                # Tong part na to dapat once lang mag execute
            elif sonos_command == "christmas":
                print("Execute christmas function")
                # Tong part na to dapat once lang mag execute
            elif sonos_command == "mellow":
                print("Execute mellow function")
        else:
            print("Nothing to be executed")
    else:
        return False


executing()


# Please workout on the checking the latest email function above and below are the Sonos related function
##########################################################################################################

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


# Choose manually
def do_it_manually():
    while True:
        choice = input("Choose one! \nPress 1 and Enter for Christmas songs.\nPress 2 and Enter for Mellow songs.\n: ")
        if choice == "1":
            play_christmas()
            print("Gotcha!")
            break
        else:
            play_english_oldies()
            print("Gotcha!")
            break


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
        # do_it_manually()
