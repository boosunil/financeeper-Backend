import json
import re
from rest_framework.response import Response as DjangoResponse
from django.utils import six
from rest_framework.serializers import Serializer
from rest_framework.utils.serializer_helpers import ReturnDict, ReturnList
from rest_framework.exceptions import\
    (
        NotAuthenticated,
        AuthenticationFailed,
        NotFound,
        ValidationError,
        ErrorDetail
    )
from rest_framework.views import exception_handler
from rest_framework.utils.serializer_helpers import ReturnDict


def base_exception_handler(exc, context):
    # Call DRF's default exception handler first,
    # to get the standard error response.
    response = exception_handler(exc, context)

    if response is None:
        return response

    print("\n")
    print("Response Type", type(response.data))
    print("\n")
    print("Is validation instance ?", isinstance(exc, ValidationError))
    print("-"*100)
    print("Error", response.data)
    print("-"*100)

    resp = {
        'data': {},
        'error': {},
        'success': False
    }

    if isinstance(response.data, (dict or ReturnDict)):
        for key, val in response.data.items():

            if isinstance(val, ReturnDict):
                for fld, err in val.items():
                    if isinstance(err, list):
                        val[fld] = err[0]

            if isinstance(val, list):
                # Indexed erorr message w/o key in case
                # non field validation
                if val:
                    if not isinstance(exc, ValidationError):
                        response.data = val
                    else:
                        response.data[key] = val
            # Django field value structure always as list
            # but in case of custom it may spit key value respons
            if not isinstance(exc, ValidationError):
                response.data = val

    if not isinstance(exc, ValidationError):
        resp['error']['message'] = response.data

    else:
        resp['error'] = response.data

    response.data = resp
    return response


class Response(DjangoResponse):
    """
    An HttpResponse that allows its data to be rendered into
    arbitrary media types.
    """

    def __init__(self, data=None, status=None,
                 template_name=None, headers=None,
                 exception=False, content_type=None):
        """
        Alters the init arguments slightly.
        For example, drop 'template_name', and instead use 'data'.

        Setting 'renderer' and 'media_type' will typically be deferred,
        For example being set automatically by the `APIView`.
        """
        super(Response, self).__init__(None, status=status)

        if isinstance(data, Serializer):
            msg = (
                'You passed a Serializer instance as data, but '
                'probably meant to pass serialized `.data` or '
                '`.error`. representation.'
            )
            raise AssertionError(msg)

        if exception is not None:
            exception = {"success": False, "data": exception}

        if isinstance(data, dict) or isinstance(data, list):
            data = {"success": True, "data": data}

        elif isinstance(data, ReturnList) or isinstance(data, ReturnDict):
            data = {"success": True, "data": data}

        else:
            data = {"success": True, "data": data}

        self.data = data
        self.template_name = template_name
        self.exception = exception
        self.content_type = content_type

        if headers:
            for name, value in six.iteritems(headers):
                self[name] = value


def multipart_viewset_parser(request):
    request.data._mutable = True
    request._full_data = request.data.dict()
    for key, value in request.data.items():
        if isinstance(value, str) and re.match(r'^\[(.*?)\]$', value):
            request.data[key] = json.loads(value)
    return request
