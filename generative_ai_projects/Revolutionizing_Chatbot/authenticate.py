import streamlit as st
from sqlalchemy.engine.base import Engine
import pandas as pd
import psycopg2
import urllib
from sqlalchemy import create_engine
from dotenv import load_dotenv
from sqlalchemy import text
import os


load_dotenv()

DATABASE_PASSWORD = os.getenv("neon_password")
connection=create_engine(f"postgresql://basitarif235:{DATABASE_PASSWORD}@ep-red-meadow-87151497.us-east-2.aws.neon.tech/chatbotconnection?sslmode=require",pool_pre_ping=True,pool_recycle=300)

def authenticate_user(phone_number: int,username:str):
    """
    Authenticate the user by checking if the phone number exists in the database.

    Args:
    phone_number (int): The user's phone number to be authenticated.

    Returns:
    bool: True if the phone number is found in the database, indicating successful authentication. False otherwise.

    Raises:
    Exception: An exception is raised if an error occurs during the authentication process.
    """
    try:
        
        user_data = get_data(phone_number=phone_number,username=username)
        return user_data
    except:
        return False





def input_data(phone_number:int,username:str):
    """
    Inserts a new phone number into the database.

    Args:
        phone_number (int): The phone number to be inserted into the database.

    Returns:
        bool: True if the phone number is successfully inserted, False otherwise.

    Raises:
        Exception: An exception is raised if an error occurs during the insertion process.
    """
    try:
        conn = connection.connect()
        conn.execute(text(f"INSERT INTO streamlitapp2 (phone_number,username) VALUES ('{phone_number}','{username}')"))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        conn.rollback()
        print(f"Error occurred while inserting data: {e}")
        return False



def get_data(phone_number:int,username) -> bool:
    """
    Retrieves data based on the provided phone number and username from the database.

    Args:
        phone_number (int): The phone number used to fetch data from the database.
        username (str): The username used to fetch data from the database.

    Returns:
        bool: True if data exists for the specified phone number and username, False otherwise.

    Raises:
        Exception: An exception is raised if an error occurs during data retrieval.
    """
    try:
        conn = connection.connect()
        data = conn.execute(text(f"SELECT * FROM streamlitapp2 WHERE phone_number='{phone_number}' and username='{username}'"))
        result = data.fetchall()
       
        if len(result) > 0:
            conn.close()
            return True
        else:
            conn.close()
            return False
    except Exception as e:
        print(f"Error occurred while fetching data: {e}")
        return False




def get_thread_key(phone_number:int):
    """
    Retrieves the thread key associated with the provided phone number from the database.

    Args:
    - phone_number (int): The phone number used to retrieve the thread key.

    Returns:
    - str or None: Returns the thread key if found, otherwise returns None.
    """
    try:
        conn = connection.connect()
        key = conn.execute(text(f"SELECT thread_key FROM thread_save WHERE phone_number='{phone_number}'"))
        result = key.fetchone()
        conn.commit()
        conn.close()
        return str(result[0]) if result else None
    except Exception as e:
        conn.rollback()
        print(f"Error occurred while fetching thread key: {e}")
        return None



def put_thread_key(phonenumber:int,thread_key:str):
    """
    Inserts a thread key associated with the provided phone number into the database.

    Args:
    - phonenumber (int): The phone number associated with the thread key.
    - thread_key (str): The thread key to be inserted into the database.

    Returns:
    - bool: Returns True if the thread key is successfully inserted, otherwise returns False.
    """
    try:
        conn = connection.connect()
        query = conn.execute(text(f"INSERT INTO thread_save (phone_number, thread_key) VALUES ('{phonenumber}',{thread_key})"))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        conn.rollback()
        conn.close()
        print(f"Error occurred while inserting thread key: {e}")
        return False

def get_limit_message(phonenumber: int):
    """
    Retrieves the counter value associated with the provided phone number and checks if it's below the limit.

    Args:
    - phonenumber (int): The phone number used to fetch the counter value.

    Returns:
    - tuple: Returns a tuple containing a boolean indicating if the counter is below the limit and the counter value itself.
    """
    conn = connection.connect()
    counter = conn.execute(text(f"SELECT Counter FROM message_limit WHERE phone_number='{phonenumber}'")).scalar()

    if counter is not None:
        is_below_limit = counter < 20
        conn.close()
        return is_below_limit, counter
    else:
        conn.close()
        return False, 0

def set_initial_limit(phonenumber: int):
    """
    Sets the initial counter value to 0 for the provided phone number in the 'message_limit' table.

    Args:
    - phonenumber (int): The phone number for which the initial counter value is to be set.

    Returns:
    - bool: Returns True if the initial counter value is successfully set to 0, otherwise returns False.
    """
    try:
        conn = connection.connect()
        initial_counter = conn.execute(text(f"INSERT INTO message_limit(phone_number, counter) VALUES ('{phonenumber}', 0)"))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        conn.rollback()
        conn.close()
        # Handle exceptions here (e.g., unique key violation, connection error, etc.)
        print(f"An error occurred: {e}")
        return False

def update_limit_counter(phonenumber:int,new_counter:int):
    """
    Updates the counter value for a given phone number in the 'message_limit' table if the new value is less than 20.

    Args:
    - phonenumber (int): The phone number associated with the counter.
    - new_counter (int): The new counter value to be updated.

    Returns:
    - str or int: Returns the updated counter value if the new value is less than 20, else returns a message indicating the limit is reached.
    """
    if new_counter < 20:
        try:
            conn = connection.connect()
            conn.execute(text(f"UPDATE message_limit SET Counter={new_counter} WHERE phone_number='{phonenumber}'"))
            conn.commit()
            conn.close()
            return new_counter
        except Exception as e:
            conn.rollback()
            conn.close()
            print(f"Error occurred while updating counter: {e}")
            return "Error occurred while updating counter"
    else:
        return "Limit reached!"


# obj1=get_data('90','bast')
# print(obj1)