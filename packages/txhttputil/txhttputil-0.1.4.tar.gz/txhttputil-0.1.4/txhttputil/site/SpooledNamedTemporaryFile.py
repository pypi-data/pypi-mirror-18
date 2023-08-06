from tempfile import SpooledTemporaryFile, NamedTemporaryFile


class SpooledNamedTemporaryFile(SpooledTemporaryFile):
    """Temporary file wrapper, specialized to switch from BytesIO
    or StringIO to a real file when it exceeds a certain size or
    when a fileno or name is needed.
    """


    def rollover(self):
        if self._rolled:
            return
        file = self._file
        self._file = NamedTemporaryFile(**self._TemporaryFileArgs)
        del self._TemporaryFileArgs

        self._file.write(file.getvalue())
        self._file.seek(file.tell(), 0)

        self._rolled = True

    @property
    def name(self):
        """ Name

        Trying to access "name" will cause the file to roll over
        """
        self.rollover()
        return self._file.name
