import abc
import typing
import warnings

from .tool_options import ToolOption
from forseti import worker


class AbsTool(metaclass=abc.ABCMeta):
    name = None  # type: str
    description = None  # type: str

    def __init__(self) -> None:
        super().__init__()
        self.options = []  # type: ignore

    @abc.abstractmethod
    def new_job(self) ->typing.Type[worker.ProcessJob]:
        pass


    @staticmethod
    @abc.abstractmethod
    def discover_jobs(*args, **kwargs):
        pass


    @staticmethod
    @abc.abstractmethod
    def get_user_options()->typing.List[ToolOption]:
        pass

    @staticmethod
    def validate_args(*args, **kwargs):
        return True

    @staticmethod
    def on_completion(*args, **kwargs):
        print("args = {}".format(args))
        print("kwargs = {}".format(kwargs))
        print("Completed")

    @staticmethod
    def generate_report(*args, **kwargs):
        return None