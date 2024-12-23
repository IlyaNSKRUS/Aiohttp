import json

def get_http_error(error_cls, message):
    message = {'error': message}
    message = json.dumps(message)
    error = error_cls(text=message, content_type='application/json')
    raise error