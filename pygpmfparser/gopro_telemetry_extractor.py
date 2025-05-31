from .gpmf_bindings import GPMFStreamCtx
from .gpmf_sample import GPMFSample

class GoProTelemetryExtractor:
    """
    A Pythonic wrapper for parsing GPMF data from GoPro MP4 files, mimicking GPMFParser.
    """

    def __init__(self, filepath: str):
        """
        Initializes the parser with an MP4 file path.

        :param filepath: Path to the MP4 file containing GPMF data.
        """
        if not isinstance(filepath, str):
            raise TypeError("filepath must be a string.")
        self._filepath = filepath
        self._ctx = None

    def _ensure_ctx(self):
        if self._ctx is None:
            self._ctx = GPMFStreamCtx(self._filepath)
        return self._ctx

    def validate(self, recurse=True):
        """
        Validates the GPMF data in the MP4 file.
        Raises an exception if validation fails.
        """
        return self._ensure_ctx().validate()

    def __iter__(self):
        """Iterates over GPMF keys and their data."""
        with GPMFStreamCtx(self._filepath) as ctx:
            while ctx.next_key():
                key_fourcc = ctx.get_key_fourcc()
                info = ctx.get_key_info()
                raw_data = ctx.get_raw_data()

                yield GPMFSample(
                    key_fourcc=key_fourcc,
                    type_char=info["type_char"],
                    type_string=info["type_string"],
                    struct_size=info["struct_size"],
                    repeat=info["repeat"],
                    samples=info["samples"],
                    raw_data=raw_data
                )

    def get_all_samples(self):
        """Returns a list of all GPMFSample objects."""
        return list(self)

    def __enter__(self):
        if self._ctx is not None:
            raise RuntimeError("Parser context already active. Use 'for sample in parser:' for iteration.")
        self._ctx = GPMFStreamCtx(self._filepath)
        self._ctx.__enter__()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._ctx:
            self._ctx.__exit__(exc_type, exc_val, exc_tb)
            self._ctx = None