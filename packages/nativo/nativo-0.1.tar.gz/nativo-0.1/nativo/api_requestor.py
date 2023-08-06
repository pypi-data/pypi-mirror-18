import calendar
import datetime
import platform
import time

try:
    from urllib.parse import urlsplit, urlunsplit, urlencode
except ImportError:
    from urllib import urlsplit, urlunsplit, urlencode

import nativo
from nativo import error, http_client, version, util


def _encode_datetime(dttime):
    if dttime.tzinfo and dttime.tzinfo.utcoffset(dttime) is not None:
        utc_timestamp = calendar.timegm(dttime.utctimetuple())
    else:
        utc_timestamp = time.mktime(dttime.timetuple())

    return int(utc_timestamp)


def _encode_nested_dict(key, data, fmt='%s[%s]'):
    d = {}
    for subkey, subvalue in data.iteritems():
        d[fmt % (key, subkey)] = subvalue
    return d


def _api_encode(data):
    for key, value in data.iteritems():
        key = util.utf8(key)
        if value is None:
            continue
        elif hasattr(value, 'nativo_id'):
            yield (key, value.nativo_id)
        elif isinstance(value, list) or isinstance(value, tuple):
            for sv in value:
                if isinstance(sv, dict):
                    subdict = _encode_nested_dict(key, sv, fmt='%s[][%s]')
                    for k, v in _api_encode(subdict):
                        yield (k, v)
                else:
                    yield ("%s[]" % (key,), util.utf8(sv))
        elif isinstance(value, dict):
            subdict = _encode_nested_dict(key, value)
            for subkey, subvalue in _api_encode(subdict):
                yield (subkey, subvalue)
        elif isinstance(value, datetime.datetime):
            yield (key, _encode_datetime(value))
        else:
            yield (key, util.utf8(value))


def _build_api_url(url, query):
    scheme, netloc, path, base_query, fragment = urlsplit(url)

    if base_query:
        query = '%s&%s' % (base_query, query)

    return urlunsplit((scheme, netloc, path, query, fragment))


class APIRequestor(object):

    def __init__(self, client=None, api_base=None):
        self.api_base = api_base or nativo.api_base
        self.api_key = nativo.api_key
        self.secret = nativo.api_secret

        from nativo import verify_ssl_certs as verify
        from nativo import proxy

        self._client = client or nativo.default_http_client or \
            http_client.new_default_http_client(
                verify_ssl_certs=verify, proxy=proxy)

    def request(self, method, url, params=None, headers=None):
        rbody, rcode, rheaders = self.request_raw(
            method.lower(), url, params, headers)
        resp = self.interpret_response(rbody, rcode, rheaders)
        return resp

    def handle_api_error(self, rbody, rcode, resp, rheaders):
        if rcode == 429:
            raise error.RateLimitError(
                self.error_message(resp), rbody, rcode, resp, rheaders)
        elif rcode in [400, 404]:
            raise error.InvalidRequestError(
                self.error_message(resp), '', rbody, rcode, resp, rheaders)
        elif rcode == 401:
            raise error.AuthenticationError(
                self.error_message(resp), rbody, rcode, resp, rheaders)
        elif rcode == 403:
            raise error.PermissionError(
                self.error_message(resp), rbody, rcode, resp, rheaders)
        else:
            raise error.APIError(
                self.error_message(resp), rbody, rcode, resp, rheaders)

    def error_message(self, resp):
        messages = resp.get('messages', [])
        if len(messages) == 1:
            return messages[0]['text']
        else:
            sorted_messages = {
                'info': [],
                'warning': [],
                'error': [],
            }
            for m in messages:
                if m.get('text'):
                    sorted_messages[m.get('level', 'info')].append(m.get('text'))

            for level in ('error', 'warning', 'info'):
                if sorted_messages[level]:
                    return sorted_messages[level][0]

        return 'Unknown Error'

    def request_raw(self, method, url, params=None, supplied_headers=None):
        """Mechanism for issuing an API call."""
        if self.api_key:
            my_api_key = self.api_key
        else:
            from nativo import api_key
            my_api_key = api_key

        if my_api_key is None:
            raise error.AuthenticationError(
                'No API key provided. (HINT: set your API key using '
                '"nativo.api_key = <API-KEY>"). You can generate API keys '
                'from the Nativo admin.  See https://developer.nativo.com/ '
                'for details, or email support@nativo.com if you have any '
                'questions.')

        abs_url = '%s%s' % (self.api_base, url)

        headers = self.request_headers(supplied_headers)

        if method == 'get' or method == 'delete':
            if params:
                encoded_params = urlencode(list(_api_encode(params or {})))
                abs_url = _build_api_url(abs_url, encoded_params)
            post_data = None
        elif method == 'post':
            post_data = util.json.dumps(params)
        else:
            raise error.APIConnectionError(
                'Unrecognized HTTP method %r.  This may indicate a bug in the '
                'Nativo bindings.  Please contact support@nativo.com for '
                'assistance.' % (method,))

        rbody, rcode, rheaders = self._client.request(
            method, abs_url, headers, post_data)

        util.logger.info('%s %s %d', method.upper(), abs_url, rcode)
        util.logger.debug(
            'API request to %s returned (response code, response body) of '
            '(%d, %r)',
            abs_url, rcode, rbody)
        return rbody, rcode, rheaders

    def request_headers(self, supplied_headers):
        from nativo.auth import auth_headers
        ua = {
            'bindings_version': version.VERSION,
            'lang': 'python',
            'publisher': 'nativo',
            'httplib': self._client.name,
        }
        for attr, func in [['lang_version', platform.python_version],
                           ['platform', platform.platform],
                           ['uname', lambda: ' '.join(platform.uname())]]:
            try:
                val = func()
            except Exception as e:
                val = "!! %s" % (e,)
            ua[attr] = val

        headers = {
            'X-Nativo-Client-User-Agent': util.json.dumps(ua),
            'User-Agent': 'Nativo/v2 PythonBindings/%s' % (version.VERSION,)
        }

        headers.update(auth_headers(self.api_key, self.secret))
        headers['Content-Type'] = 'application/json'

        if supplied_headers is not None:
            for key, value in supplied_headers.iteritems():
                headers[key] = value

        return headers

    def interpret_response(self, rbody, rcode, rheaders):
        try:
            if hasattr(rbody, 'decode'):
                rbody = rbody.decode('utf-8')
            resp = util.json.loads(rbody)
        except Exception:
            raise error.APIError(
                "Invalid response body from API: %s "
                "(HTTP response code was %d)" % (rbody, rcode),
                rbody, rcode, rheaders)
        if not (200 <= rcode < 300):
            self.handle_api_error(rbody, rcode, resp, rheaders)
        elif not resp.get('status', '') == 'success':
            rcode = resp.get('status_code')
            self.handle_api_error(rbody, rcode, resp, rheaders)
        return resp.get('data')
