import urllib
import sys

from nativo import api_requestor, error, util


class NativoObject(dict):
    def __init__(self, id=None, **params):
        super(NativoObject, self).__init__()
        self._retrieve_params = params

        if id:
            self['id'] = id

    def __setattr__(self, k, v):
        if k[0] == '_' or k in self.__dict__:
            return super(NativoObject, self).__setattr__(k, v)

        self[k] = v
        return None

    def __getattr__(self, k):
        if k[0] == '_':
            raise AttributeError(k)

        try:
            return self[k]
        except KeyError as err:
            raise AttributeError(*err.args)

        return None

    def __delattr__(self, k):
        if k[0] == '_' or k in self.__dict__:
            return super(NativoObject, self).__delattr__(k)
        else:
            del self[k]

    def __setitem__(self, k, v):
        if v == "":
            raise ValueError(
                "You cannot set %s to an empty string. "
                "We interpret empty strings as None in requests."
                "You may set %s.%s = None to delete the property" % (
                    k, str(self), k))

        super(NativoObject, self).__setitem__(k, v)

    def __getitem__(self, k):
        try:
            return super(NativoObject, self).__getitem__(k)
        except KeyError as err:
            raise err

    def __delitem__(self, k):
        super(NativoObject, self).__delitem__(k)

    @classmethod
    def api_base(cls):
        return None

    def request(self, method, url, params=None, headers=None):
        if params is None:
            params = self._retrieve_params
        requestor = api_requestor.APIRequestor(api_base=self.api_base())
        response = requestor.request(method, url, params, headers)
        return response

    def __repr__(self):
        ident_parts = [type(self).__name__]

        if isinstance(self.get('object'), basestring):
            ident_parts.append(self.get('object'))

        if isinstance(self.get('id'), basestring):
            ident_parts.append('id=%s' % (self.get('id'),))

        unicode_repr = '<%s at %s> JSON: %s' % (
            ' '.join(ident_parts), hex(id(self)), str(self))

        if sys.version_info[0] < 3:
            return unicode_repr.encode('utf-8')
        else:
            return unicode_repr

    def __str__(self):
        return util.json.dumps(self, sort_keys=True, indent=2)

    @property
    def nativo_id(self):
        return self.id


class APIResource(NativoObject):

    @classmethod
    def retrieve(cls, id, **params):
        instance = cls(id, **params)
        instance.refresh()
        return instance

    def refresh(self):
        self.refresh_from(self.request('get', self.instance_url()))
        return self

    @classmethod
    def class_name(cls):
        if cls == APIResource:
            raise NotImplementedError(
                'APIResource is an abstract class.  You should perform '
                'actions on its subclasses (e.g. Advertiser, Campaign)')
        return str(urllib.quote_plus(cls.__name__.lower()))

    @classmethod
    def class_url(cls):
        cls_name = cls.class_name()
        return "/v2/%ss" % (cls_name,)

    def instance_url(self):
        id = self.get('id')
        if not id:
            raise error.InvalidRequestError(
                'Could not determine which URL to request: %s instance '
                'has invalid ID: %r' % (type(self).__name__, id), 'id')
        id = util.utf8(id)
        base = self.class_url()
        extn = urllib.quote_plus(id)
        return "%s/%s" % (base, extn)


# Classes of API operations
class ListableAPIResource(APIResource):

    @classmethod
    def list(cls, **params):
        requestor = api_requestor.APIRequestor(api_base=cls.api_base())
        url = cls.class_url()
        response = requestor.request('get', url, params)
        return response


class ReportAPIResource(APIResource):

    @classmethod
    def retrieve(cls, **params):
        requestor = api_requestor.APIRequestor(api_base=cls.api_base())
        url = cls.class_url()
        response = requestor.request('post', url, params)
        return response


# API objects
class Advertiser(ListableAPIResource):
    @classmethod
    def class_url(cls):
        return '/v2/advertisers'


class Campaign(ListableAPIResource):
    @classmethod
    def class_url(cls):
        return '/v2/campaigns'


class DirectReport(ReportAPIResource):
    @classmethod
    def class_url(cls):
        return '/v2/data/direct'


class ManagedReport(ReportAPIResource):
    @classmethod
    def class_url(cls):
        return '/v2/data/managed'


class PreferredReport(ReportAPIResource):
    @classmethod
    def class_url(cls):
        return '/v2/data/preferred'


class MarketplaceReport(ReportAPIResource):
    @classmethod
    def class_url(cls):
        return '/v2/data/marketplace'
