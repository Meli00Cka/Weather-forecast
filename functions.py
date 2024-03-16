# Import
import random

import time




##### Functions

# sleep_timer
def sleep_timer(min, max):
    
    """
    
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
    
    """_summary_
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
    """_summary_
    
    Converts Kelvin to Celsius

    Args:
        k (_type_): int, float

    Returns:
        _type_: int, float
    """
    return k - 273.15