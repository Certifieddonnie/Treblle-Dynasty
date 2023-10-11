""" Payload Functions """
import json
import os
import socket
from datetime import datetime


class DataBuilder:
    """ Data building class to prepare the payload,
    that will be sent to treblle
    """
    DEFAULT_SENSITIVE_FIELDS = {
        'card_number',
        'cardNumber',
        'cc',
        'ccv',
        'credit_score',
        'creditScore',
        'password',
        'password_confirmation',
        'passwordConfirmation',
        'pwd',
        'secret',
        'ssn'
    }  # List of sensitive fields to be masked

    def __init__(self, params):
        """ Initialize DataBuilder """
        self.params = params

    def call(self):
        """ Call DataBuilder """
        time_spent = self.params['ended_at'] - self.params['started_at']
        user_agent = self.params['env'].get(
            'HTTP_USER_AGENT', '')  # User agent
        ip = self.calculate_ip(self.params['env'].get(
            'action_dispatch.remote_ip', ''))  # IP address
        request_method = self.params['env'].get('REQUEST_METHOD', '')
        project_id = os.environ.get('TREBLLE_PROJECT_ID', '')
        request_body = (
            json.dumps(self.safe_to_json(
                self.params['request'].query_parameters))
            if request_method.lower() == 'get'
            else json.dumps(self.safe_to_json(self.params['request'].raw_post))
        )  # Request body

        data = {
            'api_key': os.environ.get('TREBLLE_API_KEY', ''),
            'project_id': project_id,
            'version': '1.0.0',
            'sdk': 'python',
            'data': {
                'server': {
                    'ip': self.server_ip(),
                    'timezone': os.environ.get('SERVER_TIMEZONE', 'UTC'),
                    'software': self.params['headers'].get('SERVER_SOFTWARE', ''),
                    'signature': '',
                    'protocol': self.params['headers'].get('SERVER_PROTOCOL', ''),
                    'os': {},
                },
                'language': {
                    'name': 'python',
                    'version': '3.10.12',  # Replace with your Python version
                },
                'request': {
                    'timestamp': datetime.utcfromtimestamp(self.params['started_at']).strftime('%Y-%m-%d %H:%M:%S'),
                    'ip': ip,
                    # Access the URL from the Request object
                    'url': self.params['request'].url._url,
                    'user_agent': user_agent,
                    'method': request_method,
                    'headers': self.request_headers(),
                    'body': self.without_sensitive_attrs(request_body),
                },
                'response': {
                    'headers': self.params['headers'] or {},
                    'code': self.params['status'],
                    'size': len(json.dumps(self.without_sensitive_attrs(self.params['json_response']))),
                    'load_time': time_spent,
                    'body': self.without_sensitive_attrs(json.dumps(self.params['json_response'])),
                    'errors': self.build_error_object(self.params['exception']),
                },
            },
        }  # Payload to be sent to Treblle

        try:
            return json.dumps(data)  # Return payload as JSON
        except Exception:
            return json.dumps(data)  # Return payload as JSON

    def without_sensitive_attrs(self, obj):
        """ Mask sensitive attributes """
        if not obj:
            return {}
        try:
            data = json.loads(obj)
        except Exception as e:
            print(e)
            return {}
        return self.process_data(data)

    def process_data(self, data):
        """ Process data recursively """
        if isinstance(data, dict):
            return {k: self.process_data(v) for k, v in data.items()}
        elif isinstance(data, list):
            return [self.process_data(item) for item in data]
        elif isinstance(data, str) and data in self.sensitive_attrs():
            return '*' * len(data)
        else:
            return data

    def sensitive_attrs(self):
        """ Get sensitive attributes """
        return self.user_sensitive_fields().union(self.DEFAULT_SENSITIVE_FIELDS)

    def user_sensitive_fields(self):
        fields = os.environ.get(
            'TREBLLE_SENSITIVE_FIELDS', '').replace(' ', '')
        return set(fields.split(','))

    def build_error_object(self, exception):
        """ Build error object """
        if not exception:
            return []

        return [
            {
                'source': 'onError',
                'type': str(type(exception)) if exception else 'Unhandled error',
                'message': str(exception) if exception else '',
                'file': (exception.__traceback__.tb_frame.f_globals.get('__file__') if exception.__traceback__ else ''),
            }
        ]  # Error object

    def server_ip(self):
        """ Get server IP """
        for ai in socket.getaddrinfo(socket.gethostname(), None):
            if ai[1] == socket.SOCK_STREAM:
                return ai[4][0]
        # Return localhost if unable to get server IP
        return '127.0.0.1'

    def request_headers(self):
        """ Get request headers """
        if not self.params['request']:
            return {}
        return {key: value for key, value in self.params['request'].headers.env.items() if '.' not in key}

    def safe_to_json(self, obj):
        """ Convert to JSON """""
        try:
            return json.loads(obj)
        except Exception:
            return {}

    def calculate_ip(self, remote_ip):
        """ Calculate IP """
        if remote_ip:
            return remote_ip  # Return remote IP if available

        server_ip = socket.gethostbyname(socket.gethostname())  # Server IP
        return server_ip
