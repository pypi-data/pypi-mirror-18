URL = "https://www.google.com/recaptcha/api/siteverify"
error_mapping = {"missing-input-secret": "The secret parameter is missing.",
                 "invalid-input-secret": "The secret parameter is invalid or malformed.",
                 "missing-input-response": "The response parameter is missing.",
                 "invalid-input-response": "The response parameter is invalid or malformed."}


class Verifier:
    def __init__(self, secret=None, response=None, remote_ip=None):
        self.request_data = {}
        self.response = None
        self.errors = []
        self.request_data = {'secret': secret, 'response': response}
        if remote_ip:
            self.request_data['remoteip'] = remote_ip

    def verify(self):
        import logging
        from google.appengine.api.urlfetch import fetch, POST, Error
        from json import loads
        try:
            from urllib import urlencode
            payload = urlencode(self.request_data)
            headers = {'Content-Type': 'application/x-www-form-urlencoded'}
            response = fetch(URL, method=POST, headers=headers, payload=payload)
            self.response = loads(response.content)
            if self.response['success']:
                return True
            else:
                self.errors = map(lambda key: error_mapping[key], self.response['error-codes'])
                # Put all the error messages in a list
                return False
        except Error:
            logging.exception('Exception when fetching url')