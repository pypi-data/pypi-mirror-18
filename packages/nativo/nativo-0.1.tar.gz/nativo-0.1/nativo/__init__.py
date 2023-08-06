api_key = None
api_secret = None
api_base = 'https://dev-api.nativo.net'
api_version = None
verify_ssl_certs = False
proxy = None
default_http_client = None

# Resource
from nativo.resource import (  # noqa
    Advertiser,
    Campaign,
    DirectReport)

# Error imports.  Note that we may want to move these out of the root
# namespace in the future and you should prefer to access them via
# the fully qualified `nativo.error` module.

from nativo.error import (  # noqa
    APIConnectionError,
    APIError,
    AuthenticationError,
    PermissionError,
    RateLimitError,
    InvalidRequestError,
    NativoError)

from nativo.version import VERSION  # noqa
from nativo.api_requestor import APIRequestor  # noqa
from nativo.resource import (  # noqa
    APIResource,
    ListableAPIResource,
    NativoObject)
from nativo.util import json, logger  # noqa
