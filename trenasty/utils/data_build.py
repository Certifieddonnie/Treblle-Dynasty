""" Payload Functions """
import json
import socket
from datetime import datetime
import platform
from trenasty.configs.config import TREBLLE_SENSITIVE_KEYS, TREBLLE_PROJECT_ID, TREBLLE_API_KEY


class DataBuilder:
    """ Data building class to prepare the payload/data,
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
        project_id = TREBLLE_PROJECT_ID
        api_key = TREBLLE_API_KEY
        if not project_id or not api_key:
            return
        time_spent = self.params['ended_at'] - self.params['started_at']
        user_agent = self.params['env'].get(
            'HTTP_USER_AGENT', '')  # Get User agent value from request.scope attribute
        ip = self.fetch_ip(self.params['env'].get(
            'CLIENT', '')[0])  # Get IP address from request.scope attribute
        request_method = self.params['env'].get('REQUEST_METHOD', '')
        request_body = (
            json.dumps(self.safe_to_json(
                self.params['request'].query_parameters))
            if request_method.lower() == 'get'
            else json.dumps(self.safe_to_json(self.params['request'].raw_post))
        )  # Request body

        data = {
            'api_key': api_key,
            'project_id': project_id,
            'version': '0.6',
            'sdk': 'python-fastapi',
            'data': {
                'server': {
                    'ip': self.server_ip(),
                    'timezone': datetime.now().astimezone().tzinfo,
                    'software': self.params['headers'].get('SERVER_SOFTWARE', ''),
                    'signature': '',
                    'protocol': self.params['headers'].get('SERVER_PROTOCOL', ''),
                    'os': {
                        "name": platform.system(),
                        "release": platform.release(),
                        "architecture": platform.machine(),
                        "version": platform.version(),
                    },
                },
                'language': {
                    'name': 'python',
                    'version': '3.10.12',  # Python Version
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
        }  # Payload/Data to be sent to Treblle

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
        # sensitive_fields = set("pwdssncard_numberccv")
        # data = {"name": "John", "age": 30, "pwd": "123456JKL"}
        # "name": "John", "age": 30, "pwd": "*********"
        else:
            return data

    def sensitive_attrs(self):
        """ Get sensitive attributes """
        return self.user_sensitive_fields().union(self.DEFAULT_SENSITIVE_FIELDS)

    def user_sensitive_fields(self):
        """ Get user sensitive fields """
        fields = TREBLLE_SENSITIVE_KEYS.replace(' ', '')
        # fields = "pwd ssn card_number ccv"
        # fields = "pwdssncard_numberccv"
        # fields = "pwd,ssn,card_number,ccv
        # fields = (pwd,ssn,card_number,ccv)
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
        for addr in socket.getaddrinfo(socket.gethostname(), None):
            # addr = tuple of (family, type, proto, canonname, sockaddr[ip, port])
            if addr[1] == socket.SOCK_STREAM:
                # if addr[1] is socket.SOCK_STREAM, then it is IPv4 operating on TCP Network
                # returning the IP address from the sockaddr tuple (addr[4][0])
                return addr[4][0]
        # Return localhost if unable to get server IP
        return '127.0.0.1'

    def request_headers(self):
        """ Get request headers """
        if not self.params['request']:
            return {}
        # Return request headers without '.' in the key name (to avoid error) and convert to dictionary format (key-value pair)
        return {key: value for key, value in self.params['request'].headers.env.items() if '.' not in key}

    def safe_to_json(self, obj):
        """ Convert to JSON """""
        try:
            return json.loads(obj)
        except Exception:
            return {}

    def fetch_ip(self, remote_ip):
        """ Fetch Host IP """
        if remote_ip:
            return remote_ip  # Return remote IP if available
        # Return server IP if remote IP is not available (e.g. in localhost)

        server_ip = socket.gethostbyname(socket.gethostname())  # Server IP
        #
        return server_ip
