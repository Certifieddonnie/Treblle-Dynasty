""" Configuration File """
from dotenv import load_dotenv, find_dotenv
import os

load_dotenv(find_dotenv())


# Configuration Variables
TREBLLE_API_KEY = os.environ.get('TREBLLE_API_KEY')
TREBLLE_PROJECT_ID = os.environ.get('TREBLLE_PROJECT_ID')
TREBLLE_SENSITIVE_KEYS = os.environ.get('TREBLLE_SENSITIVE_KEYS')
TIME_ZONE = os.environ.get('TIME_ZONE')
if TIME_ZONE is None:
    TIME_ZONE = 'UTC'


# Treblle sensitive keys = "pwd,password,..."
