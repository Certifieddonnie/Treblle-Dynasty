import json
import os
import threading
import requests
from datetime import datetime
from time import time
from fastapi import FastAPI, Request
from trenasty.utils.data_build import DataBuilder
from trenasty.utils.helper import load_balancer


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
            status = response.status_code  # Status code of response
            headers = response.headers  # Headers of response
            to_parse = response.text  # Response body

            try:
                json_response = json.loads(to_parse)  # Parse response to JSON
            except (json.JSONDecodeError, TypeError):
                # Continue with original values when unable to parse response to JSON
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
            }
            # Send error payload to Treblle, but raise the exception as well
            self.capture(params)
            raise e

        return response

    def capture(self, params):
        """ Capture data and send to Treblle """
        data = DataBuilder(params).call()
        # Ignore capture for unnaturally large requests
        if data and len(data.encode()) > 2 * 1024 * 1024:
            return

        threading.Thread(target=self.send_to_treblle, args=(
            data,)).start()  # Send data to Treblle

    def send_to_treblle(self, data):
        """ Send data to Treblle """
        uri = self.TREBLLE_URI
        headers = {
            'Content-Type': 'application/json',
            'x-api-key': os.environ.get('TREBLLE_API_KEY', '')
        }  # Headers for Treblle request
        try:
            # Send data to Treblle
            res = requests.post(uri, data=data, headers=headers)
            print(res.text)  # Print Treblle response
        except Exception as e:
            print(e)

    def status_code_for_exception(self, exception):
        """ Get status code for exception """
        try:
            return exception.status_code
        except:
            return 500
