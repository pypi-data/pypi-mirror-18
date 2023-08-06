import logging
import os

from twisted.web.resource import NoResource

from txhttputil.site.BasicResource import BasicResource

logger = logging.getLogger(__name__)

import mimetypes

mimetypes.init()


def get_extensions_for_type(general_type):
    for ext in mimetypes.types_map:
        if mimetypes.types_map[ext].split('/')[0] == general_type:
            yield ext


IMAGE_EXTENSIONS = list(get_extensions_for_type('image'))
FONT_EXTENSIONS = list(get_extensions_for_type('font'))


class FileUnderlayResource(BasicResource):
    """
    This class resolves URLs into either a static file or a C{BasicResource}

    This is a multi level search :
    1) getChild, looking for resource in the resource tree
    2) The staticFileUnderlay is searched.
    3) Request fails with NoResource()

    """

    acceptedExtensions = ['.js', '.css', '.html', '.xml']
    acceptedExtensions += FONT_EXTENSIONS
    acceptedExtensions += IMAGE_EXTENSIONS

    def __init__(self):
        BasicResource.__init__(self)

        self._fileSystemRoots = []

    def getChildWithDefault(self, path, request):
        return self.getChild(path, request)

    def getChild(self, path, request):
        # Optionally, Do some checking with userSession.userDetails.group
        # userSession = IUserSession(request.getSession())

        resoureFromTree = BasicResource.getChild(self, path, request)
        if not isinstance(resoureFromTree, NoResource):
            return resoureFromTree

        # else, look for it in the file system
        filePath = self.getRealFilePath(os.path.join(path, *request.postpath))
        if filePath:
            from txhttputil.site.StaticFileResource import StaticFileResource
            return self._gzipIfRequired(StaticFileResource(filePath))

        return NoResource()

    def addFileSystemRoot(self, fileSystemRoot: str):
        if not os.path.isdir(fileSystemRoot):
            raise NotADirectoryError("%s is not a directory" % fileSystemRoot)

        self._fileSystemRoots.append(fileSystemRoot)

    def getRealFilePath(self, resourcePath: str) -> str:

        for rootDir in self._fileSystemRoots[::-1]:
            realFilePath = os.path.join(rootDir, resourcePath.decode())

            if os.path.isdir(realFilePath):
                logger.debug("Resource path %s is a directory %s",
                             resourcePath, realFilePath)

            if os.path.isfile(realFilePath):
                return realFilePath
