import logging
import os

from twisted.python.compat import nativeString
from twisted.web.error import UnsupportedMethod
from twisted.web.resource import EncodingResourceWrapper, IResource, NoResource
from twisted.web.server import GzipEncoderFactory
from zope.interface import implementer

logger = logging.getLogger(__name__)

import mimetypes

mimetypes.init()


def get_extensions_for_type(general_type):
    for ext in mimetypes.types_map:
        if mimetypes.types_map[ext].split('/')[0] == general_type:
            yield ext


IMAGE_EXTENSIONS = list(get_extensions_for_type('image'))
FONT_EXTENSIONS = list(get_extensions_for_type('font'))


@implementer(IResource)
class BasicResource:
    """ Basic Resource

    This class is a node for the resource tree, It's a slightly simpler version of
    C{twisted.web.resource.Resource}

    """
    isGzipped = False
    entityType = IResource
    server = None
    isLeaf = False

    def __init__(self):
        """
        Initialize.
        """
        self.__children = {}

    def getChild(self, path, request):
        if path in self.__children:
            return self.__children[path]
        return NoResource()

    getChildWithDefault = getChild

    def putChild(self, path: bytes, child):
        if b'/' in path:
            raise Exception("Path %s can not start or end with '/' ", path)

        self.__children[path] = child
        child.server = self.server

    def deleteChild(self, path: bytes):
        if b'/' in path:
            raise Exception("Path %s can not start or end with '/' ", path)

        del self.__children[path]

    def render(self, request):
        # Optionally, Do some checking with userSession.userDetails.group
        # userSession = IUserSession(request.getSession())
        methodName = 'render_' + nativeString(request.method)

        m = getattr(self, methodName, None)
        if not m:
            raise UnsupportedMethod(methodName)
        return m(request)

    def render_HEAD(self, request):
        return self.render_GET(request)

    def _gzipIfRequired(self, resource):
        if (not isinstance(resource, EncodingResourceWrapper)
            and hasattr(resource, 'isGzipped')
            and resource.isGzipped):
            return EncodingResourceWrapper(resource, [GzipEncoderFactory()])
        return resource

