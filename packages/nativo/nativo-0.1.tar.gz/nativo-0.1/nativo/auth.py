import hashlib
import hmac
import time


def auth_headers(api_key, secret):
    """Return header data needed to authenticate each request."""
    nativo_timestamp = int(time.time())
    nativo_hash = hmac.new(api_key.encode('utf8'), (secret + str(nativo_timestamp)).encode('utf8'),
                           digestmod=hashlib.sha256).hexdigest()
    return {'nativo-token': api_key,
            'nativo-timestamp': str(nativo_timestamp),
            'nativo-hash': nativo_hash}
