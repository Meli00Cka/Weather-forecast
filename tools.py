##### Import
from dotenv import load_dotenv
import requests as req
import sqlite3
import random
import time
import re


##### Functions

def configure():    
    load_dotenv()
    
def error_msg(message: str, *args):
    print("\033[0;33m" + message, end=' ')
    for arg in args:
        print(arg, end=' ')
    print("\033[0m")


def extract_city_name(string):
    pattern = r"^.*?(?=\s-)"
    return re.search(string=string, pattern=pattern).group(0)


def send_request(base_url ,parameters=None, headers=None, json=True):
    
    print(f"sending request to: {base_url}")
    
    try:
        res = req.get(url=base_url, params=parameters, headers=headers)
        st_code = res.status_code
    
        if st_code == req.codes.ok:
            if json:
                res = res.json()
            return res
        
        else:
            error_msg("Error:", st_code, res.text)
            return False
        
    except req.exceptions.ConnectionError as e:
        error_msg(f"Connection error: {e}")
        return False
    except req.exceptions.Timeout as e:
        error_msg(f"Timeout error: {e}")
        return False
    except req.exceptions.HTTPError as e:
        error_msg(f"HTTP error: {e}")
        return False
    except req.exceptions.TooManyRedirects as e:
        error_msg(f"Too many redirects: {e}")
        return False
    except req.exceptions.RequestException as e:
        error_msg(f"An unknown error occurred: {e}")
        return False
    

def sleep_timer(min, max):
    
    """Sleeps
    
        This function generates a random number between given numbers
        then sleeps.
        
        
        Example:
        
        >>> sleep_timer(1.5, 2)
            1.9
        >>> sleep_timer(1.5, 2)
            1.6
    """
    
    if min or max == str:
        min = int(min)
        max = int(max)
    
    sleep_sec = (max-min)*random.random() + min
    time.sleep(sleep_sec)



def check_key_exists(file, key):
    
    """ Check if the given key exists or no;
    if not gives the indexes as a list
    """
    
    idx = []
    
    for i in range(len(file)):
        
        if key in file[i]:
            pass
        else:
            error_msg(f"file[{i}] doesn't have any key same as: '{key}'")
            idx.append(i)
            
    return idx


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


def handle_sql_execute(session, *queries):
    try:
        cursor = session.cursor()
        
        for query in queries:
            cursor.execute(query)
            session.commit()
        
    except sqlite3.Error as error:
        error_msg(f"Error executing database queries:\n{error}")