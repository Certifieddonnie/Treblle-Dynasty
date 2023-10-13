import json
import logging
import threading
import requests
from time import time
from fastapi import Request
from trenasty.utils.data_build import DataBuilder
from trenasty.utils.helper import load_balancer
from starlette.concurrency import iterate_in_threadpool
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

            #  # Creating Custom Headers
            # response.headers["X-Rate-Limit"] = "100"
            # response.headers["X-Api-Version"] = self.TREBLLE_VERSION
            # response.headers["Content-Type"] = "application/json"
            # response.headers["X-Content-Type-Options"] = "nosniff"
            # response.headers["X-Frame-Options"] = "deny"
            # response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains"
            # response.headers["Content-Security-Policy"] = "default-src 'self'"
            # response.headers["Accept"] = "application/json"
            # response.headers["Allow"] = "GET, POST, PUT, DELETE, OPTIONS"
            # response.headers["Access-Control-Allow-Origin"] = "*"

            # Receiving response in a raw format
            status = response.status_code  # Status code of response
            headers = response.headers  # Headers of response
            response_body = [item async for item in response.body_iterator]
            response.body_iterator = iterate_in_threadpool(iter(response_body)) # Response body iterator for response body in a raw format (bytes)
            # Response body
            if response_body:
                to_parse = (b''.join(response_body)).decode() # Convert response body to string
            to_parse = (b''.join(response_body)).decode()

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
                'exception': None,
                'headers': headers,
                'json_response': json_response,
                'request': request,
                'started_at': started_at,
                'status': status
            }  # Parameters to be passed to DataBuilder
            await self.capture(params)  # Capture data
        except Exception as e:
            status = self.status_code_for_exception(
                e)  # Status code of exception
            params = {
                'ended_at': time(),
                'env': request.scope,
                'exception': e,
                'headers': {},
                'json_response': {},
                'request': request,
                'started_at': started_at,
                'status': status
            }  # Error Parameters to be passed to DataBuilder
            # Send error payload to Treblle, but raise the exception as well
            await self.capture(params)
            raise e

        return response

    async def capture(self, params):
        """ Capture data and send to Treblle """
        data = await DataBuilder(params).call()
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
            'X-api-key': TREBLLE_API_KEY,
            'Accept': 'application/json',
            'Allow': 'GET, POST, PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Origin': '*',  # Allow all origins
            'X-Frame-Options': 'deny',
            'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
            'Content-Security-Policy': 'default-src \'self\'',
            'X-Content-Type-Options': 'nosniff',
            'X-Rate-Limit': '100',
            'Content-Encoding': 'gzip',
            # 'Accept-Encoding': 'gzip, deflate, br',
        }  # Headers for Treblle request
        try:
            # Send data to Treblle
            res = requests.post(uri, json=data, headers=headers)
            logging.info(f"{(res.content).decode('utf-8')}")  # Print Treblle response
        except Exception as e:
            logging.error(f"{e}")

    def status_code_for_exception(self, exception):
        """ Get status code for exception """
        try:
            return exception.status_code
        except:
            return 500
