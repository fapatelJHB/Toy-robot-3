"""
TODO: You can either work from this skeleton, or you can build on your solution for Toy Robot 2 exercise.
"""


# list of valid command names
valid_commands = ['off', 'help', 'forward', 'back', 'right', 'left', 'sprint', 'replay', 'replay silent', 'replay reversed', 'replay reversed silent']
silent = False
reverse = False
replay =  False
# variables tracking position and direction
position_x = 0
position_y = 0
directions = ['forward', 'right', 'back', 'left']
current_direction_index = 0

# area limit vars
min_y, max_y = -200, 200
min_x, max_x = -100, 100

history = []


def command_history(command):
    global history
    history.append(command)
    pass
    return (history)



def get_robot_name():
    name = input("What do you want to name your robot? ")
    while len(name) == 0:
        name = input("What do you want to name your robot? ")
    return name


def get_command(robot_name):
    """
    Asks the user for a command, and validate it as well
    Only return a valid command
    """

    prompt = ''+robot_name+': What must I do next? '
    command = input(prompt)
    while len(command) == 0 or not valid_command(command):
        output(robot_name, "Sorry, I did not understand '"+command+"'.")
        command = input(prompt)

    return command.lower()


def split_command_input(command):
    """
    Splits the string at the first space character, to get the actual command, as well as the argument(s) for the command
    :return: (command, argument)
    """
    args = command.split(' ', 1)
    if len(args) > 1:
        return args[0], args[1]
    return args[0], ''


def is_int(value):
    """
    Tests if the string value is an int or not
    :param value: a string value to test
    :return: True if it is an int
    """
    try:
        int(value)
        return True
    except ValueError:
        return False


def valid_command(command):
    """
    Returns a boolean indicating if the robot can understand the command or not
    Also checks if there is an argument to the command, and if it a valid int
    """

    (command_name, arg1) = split_command_input(command)
    range_arg = arg1.split('-')
    if len(range_arg) == 2 and is_int(range_arg[0]) and is_int(range_arg[1]):
        return command_name.lower() in valid_commands and len(range_arg) == 2

    return command_name.lower() in valid_commands and (len(arg1) == 0 or is_int(arg1) or arg1.lower() == 'silent' or arg1.lower() == 'reversed') or (arg1.lower() == 'reversed silent')


def output(name, message):
    print(''+name+": "+message)


def do_help():
    """
    Provides help information to the user
    :return: (True, help text) to indicate robot can continue after this command was handled
    """
    return True, """I can understand these commands:
OFF  - Shut down robot
HELP - provide information about commands
FORWARD - move forward by specified number of steps, e.g. 'FORWARD 10'
BACK - move backward by specified number of steps, e.g. 'BACK 10'
RIGHT - turn right by 90 degrees
LEFT - turn left by 90 degrees
SPRINT - sprint forward according to a formula
REPLAY - replays the commands
REPLAY SILENT -  replays the commands silently.
REPLAY REVERSED - replay the commands in reverse order.
REPLAY REVERSED SILENT - replays commans in reverse silently.
"""


def show_position(robot_name):
    print(' > '+robot_name+' now at position ('+str(position_x)+','+str(position_y)+').')


def is_position_allowed(new_x, new_y):
    """
    Checks if the new position will still fall within the max area limit
    :param new_x: the new/proposed x position
    :param new_y: the new/proposed y position
    :return: True if allowed, i.e. it falls in the allowed area, else False
    """

    return min_x <= new_x <= max_x and min_y <= new_y <= max_y


def update_position(steps):
    """
    Update the current x and y positions given the current direction, and specific nr of steps
    :param steps:
    :return: True if the position was updated, else False
    """

    global position_x, position_y
    new_x = position_x
    new_y = position_y

    if directions[current_direction_index] == 'forward':
        new_y = new_y + steps
    elif directions[current_direction_index] == 'right':
        new_x = new_x + steps
    elif directions[current_direction_index] == 'back':
        new_y = new_y - steps
    elif directions[current_direction_index] == 'left':
        new_x = new_x - steps

    if is_position_allowed(new_x, new_y):
        position_x = new_x
        position_y = new_y
        return True
    return False


def do_forward(robot_name, steps):
    """
    Moves the robot forward the number of steps
    :param robot_name:
    :param steps:
    :return: (True, forward output text)
    """
    if update_position(steps):
        return True, ' > '+robot_name+' moved forward by '+str(steps)+' steps.'
    else:
        return True, ''+robot_name+': Sorry, I cannot go outside my safe zone.'


def do_back(robot_name, steps):
    """
    Moves the robot forward the number of steps
    :param robot_name:
    :param steps:
    :return: (True, forward output text)
    """
    if update_position(-steps):
        return True, ' > '+robot_name+' moved back by '+str(steps)+' steps.'
    else:
        return True, ''+robot_name+': Sorry, I cannot go outside my safe zone.'


def do_right_turn(robot_name):
    """
    Do a 90 degree turn to the right
    :param robot_name:
    :return: (True, right turn output text)
    """
    global current_direction_index

    current_direction_index += 1
    if current_direction_index > 3:
        current_direction_index = 0

    return True, ' > '+robot_name+' turned right.'


def do_left_turn(robot_name):
    """
    Do a 90 degree turn to the left
    :param robot_name:
    :return: (True, left turn output text)
    """
    global current_direction_index

    current_direction_index -= 1
    if current_direction_index < 0:
        current_direction_index = 3

    return True, ' > '+robot_name+' turned left.'


def do_sprint(robot_name, steps):
    """
    Sprints the robot, i.e. let it go forward steps + (steps-1) + (steps-2) + .. + 1 number of steps, in iterations
    :param robot_name:
    :param steps:
    :return: (True, forward output)
    """

    if steps == 1:
        return do_forward(robot_name, 1)
    else:
        (do_next, command_output) = do_forward(robot_name, steps)
        print(command_output)
        return do_sprint(robot_name, steps - 1)

def do_replay(arg, robot_name, command):
    global silent
    global reverse
    global replay
    replay = True
    silent = False
    reverse = False
    
    if len(arg) > 0:
        arg1 = arg.lower().split()
        range_arg = arg.split('-')
    history_reversed = list(reversed(history))
    if 'replay' in command and len(arg) == 0:
        for element in history:
            replay = True
            handle_command(robot_name, element) 


    elif 'silent' in arg1 and len(arg1) == 1:
        for element in history:
            silent = True
            handle_command(robot_name, element)


    elif 'reversed' in arg1 and len(arg1) == 1:
        for element in history_reversed:
            reverse = True
            handle_command(robot_name, element)

    elif 'reversed' == arg1[0] and arg1[1] == 'silent':
        for element in history_reversed:
            reverse = True
            silent = True
            handle_command(robot_name, element)
    
    elif 'replay' in command and '-' in arg:
        range_arg = arg.split('-')
        new_list = history[-int(range_arg[0]): -int(range_arg[1])]
        for element in new_list:
            replay = True
            handle_command(robot_name, element)
        return (True, f' > {robot_name} replayed {str(len(new_list))} commands.')

    elif 'replay' in command and is_int(arg):

        new_list = history[-int(arg):]
        for element in new_list:
            replay = True
            handle_command(robot_name, element)
        return (True, f' > {robot_name} replayed {str(len(new_list))} commands.')

    elif 'replay' in command and len(arg) == 2 and is_int(arg[0]) and arg[1] == 'silent' or arg[1] == 'reversed':
        if 'silent' in arg1:
            silent = True

        if 'reversed' in arg1:
            reverse = True
            reversed(history)

        new_list = history[-int(arg):]
        for element in new_list:
            replay = True
            handle_command(robot_name, element)
        r = ''
        s = ''
        if reverse == True: r = ' in reverse'
        if silent == True: s = ' silently'
        return (True, f' > {robot_name} replayed {str(len(new_list))} commands{r}{s}.')

    r = ''
    s = ''
    if reverse == True: r = ' in reverse'
    if silent == True: s = ' silently'
    replay = False
    reverse = False
    silent = False
    return (True, f' > {robot_name} replayed {str(len(history))} commands{r}{s}.')


def handle_command(robot_name, command):
    """
    Handles a command by asking different functions to handle each command.
    :param robot_name: the name given to robot
    :param command: the command entered by user
    :return: `True` if the robot must continue after the command, or else `False` if robot must shutdown
    """

    (command_name, arg) = split_command_input(command)

    if command_name == 'off':
        return False
    elif command_name == 'help':
        (do_next, command_output) = do_help()
    elif command_name == 'forward':
        (do_next, command_output) = do_forward(robot_name, int(arg))
    elif command_name == 'back':
        (do_next, command_output) = do_back(robot_name, int(arg))
    elif command_name == 'right':
        (do_next, command_output) = do_right_turn(robot_name)
    elif command_name == 'left':
        (do_next, command_output) = do_left_turn(robot_name)
    elif command_name == 'sprint':
        (do_next, command_output) = do_sprint(robot_name, int(arg))
    elif command_name == 'replay':
        (do_next, command_output) = do_replay(arg, robot_name, command)
    if len(command) > 0 and silent==False:
        print(command_output)
        show_position(robot_name)

    return do_next


def robot_start():
    """This is the entry point for starting my robot"""

    global position_x, position_y, current_direction_index, history

    robot_name = get_robot_name()
    output(robot_name, "Hello kiddo!")

    position_x = 0
    position_y = 0
    current_direction_index = 0
    history = []

    command = get_command(robot_name)
    while handle_command(robot_name, command):
        if 'replay' not in command:
            history.append(command)
        command = get_command(robot_name)


    output(robot_name, "Shutting down..")


if __name__ == "__main__":
    robot_start()
