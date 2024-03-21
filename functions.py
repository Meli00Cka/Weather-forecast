# Import
import random

import time




##### Functions

# sleep_timer
def sleep_timer(min, max):
    
    """Sleeps
    
        This function generates a random number between given numbers
        then sleeps.
        
        
        Example:
        
        sleep_timer(1.5, 2)
        
    """
    
    if min or max == str:
        min = int(min)
        max = int(max)
    
    sleep_sec = (max-min)*random.random() + min
    time.sleep(sleep_sec)



# check_key_exists
def check_key_exists(file, key):
    
    """ Check if the given key exists or no
    This function checks if the given key exists in a data set or no,
    if not gives the indexes as a list
    """
    
    idx = []
    
    for i in range(len(file)):
        
        if key in file[i]:
            pass
        else:
            print(f"file[{i}] doesn't have any key same as: '{key}'")
            idx.append(i)
            
    return idx



def weather_convertor(k):
    """Converts Kelvin to Celsius
    
    Args:
        k (int or float): Kelvin value
        
    Returns:
        converted Celsius value
    """
    
    return k - 273.15

def error_msg(message: str):
    print("\033[0;3;33m" + message + "\033[0m")


def user_input_code(message: str):
    """Gets user input and handles input errors

    Args:
        message (str): The question you want to ask from user

    Returns:
        int: user's input
    """
    while True:
        try:
            user_input = input(f"{message}\n")
            return int(user_input)
        except ValueError:
            error_msg("A ValueError exception has been occurred, input must be an integer")
        except Exception as e:
            error_msg(f"Unexpected error occurred: {e}")
            
            