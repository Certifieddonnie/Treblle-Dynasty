import json
import logging
import threading
import requests
from time import time
from fastapi import Request
from trenasty.utils.data_build import DataBuilder
from trenasty.utils.helper import load_balancer
from trenasty.configs.config import TREBLLE_API_KEY

logging.basicConfig(
    level=logging.INFO,  # Set the logging level to ERROR
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler()],  # Output logs to the console.
)


class TreblleMiddleware:
    """ Treblle Middleware for FastAPI """
    TREBLLE_URI = load_balancer()
    TREBLLE_VERSION = '0.6'

    def __init__(self, app):
        """ Initialize Treblle Middleware """
        self.app = app

    async def __call__(self, request: Request, call_next):
        """ Call Treblle Middleware """
        started_at = time()  # Start time of request

        try:
            response = await call_next(request)  # Call next middleware
            # Receiving response in a raw format
            status = response.status_code  # Status code of response
            headers = response.headers  # Headers of response
            to_parse = response.text  # Response body

            try:
                json_response = json.loads(to_parse)  # Parse response to JSON
                # Convert from raw format to JSON
            except (json.JSONDecodeError, TypeError):
                # Continue with original values when unable to parse response to JSON
                # This is the case when response is not in JSON format, returning the raw format
                return response

            params = {
                'ended_at': time(),
                'env': request.scope,
                'headers': headers,
                'json_response': json_response,
                'request': request,
                'started_at': started_at,
                'status': status
            }  # Parameters to be passed to DataBuilder
            self.capture(params)  # Capture data
        except Exception as e:
            status = self.status_code_for_exception(
                e)  # Status code of exception
            params = {
                'ended_at': time(),
                'env': request.scope,
                'exception': e,
                'headers': {},
                'request': request,
                'started_at': started_at,
                'status': status
            }  # Error Parameters to be passed to DataBuilder
            # Send error payload to Treblle, but raise the exception as well
            self.capture(params)
            raise e

        return response

    def capture(self, params):
        """ Capture data and send to Treblle """
        data = DataBuilder(params).call()
        # data is the payload from the data_builder.py file
        # Ignore capture for unnaturally large requests
        if data and len(data.encode()) > 2 * 1024 * 1024:
            return
        if not data:
            logging.error('missing treblle api key and project id')

        treblle_thread = threading.Thread(target=self.send_to_treblle, args=(
            data,))
        # Send data to Treblle after a request is made.
        treblle_thread.start()  # Starts the thread and waits for the target function to finish

    def send_to_treblle(self, data):
        """ Send data to Treblle """
        uri = self.TREBLLE_URI
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': TREBLLE_API_KEY
        }  # Headers for Treblle request
        try:
            # Send data to Treblle
            res = requests.post(uri, data=data, headers=headers)
            logging.info(f"{res.text}")  # Print Treblle response
        except Exception as e:
            logging.error(f"{e}")

    def status_code_for_exception(self, exception):
        """ Get status code for exception """
        try:
            return exception.status_code
        except:
            return 500
