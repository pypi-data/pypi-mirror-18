# Put your commands here
COMMAND1 = "hi"
COMMAND2 = "am i a hacker?"
COMMAND3 = "who is the master"
COMMAND4 = "why do you have so many commands?"
COMMAND5 = "kecko"
COMMAND6 = "time to eat the cake!"
COMMAND7 = "name 4 names of cats"
COMMAND8 = "can I make a game?"
COMMAND9 = "yay"
COMMAND10 = "rollercoaster time"
COMMAND11 = "cake"

# Your handling code goes in this function
def handle_command(command):
    """
        Determine if the command is valid. If so, take action and return
        a response, if necessary.
    """
    response = ""
    if command.find(COMMAND1) >= 0:
        response = "Hi Minecraftman"
    
    elif command.find(COMMAND2) >= 0:
        response = "yes, you are destined to be a hackerF"
    elif command.find(COMMAND3) >= 0:
        response = "Kent is the master, all hail Kent"
    elif command.find(COMMAND4) >= 0:
        response = "the WEMS students are giving them to me"
    elif command.find(COMMAND5) >= 0:
        response = "happy birthday! @kecko made it your birthday! the next birthday command is: time to eat the cake!"
    elif command.find(COMMAND6) >= 0:
        response = "Dean stole the cake, I'll make another in 999 hours!"
    elif command.find(COMMAND7) >= 0:
        response = "Caspian and Luna -- who are Kent's cats -- and Huckle and Nugget -- who are Emerson's cats"
    elif command.find(COMMAND8) >= 0:
        response = "you can with this link https://www.makeschool.com/build-an-iphone-game-in-your-browser"
    elif command.find(COMMAND9) >=0:
        response = "you are at an amusement park! @kecko made this amusement park, the next amusement park command is rollercoaster time"
    elif command.find(COMMAND10) >=0:
        response = "the rollercoaster broke! to fix it the command is cake"
    elif command.find(COMMAND11) >=0:
        response = "JK! cake in your face!"
    return response
