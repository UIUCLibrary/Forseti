import logging
import typing
from contextlib import contextmanager

import os

from forseti import worker
from forseti.tools.abstool import AbsTool
from forseti.tools import tool_options
from forseti.worker import ProcessJob, GuiLogHandler

import packager
import packager.packages
import enum


class UserArgs(enum.Enum):
    INPUT = "Input"
    OUTPUT = "Output"


class ResultValues(enum.Enum):
    VALID = "valid"
    FILENAME = "filename"
    PATH = "path"
    CHECKSUM_REPORT_FILE = "checksum_report_file"


class JobValues(enum.Enum):
    PACKAGE = "package"
    OUTPUT = "output"
    SOURCE_PATH = "source_path"


class CaptureOneToHathiTiffPackage(AbsTool):
    name = "Convert CaptureOne TIFF to Hathi TIFF package"
    description = "Work in progress!!" \
                  "\n" \
                  "\nInput is a path to a folder of TIFF files all named with a bibID as a prefacing identifier, a " \
                  "final delimiting underscore or dash, and a sequence consisting of padded zeroes and a number." \
                  "\n" \
                  "\nOutput is a directory of folders named by bibID with the prefacing delimiter stripped from each " \
                  "filename."

    @staticmethod
    def discover_jobs(**user_args) -> typing.List[dict]:
        jobs = []
        source_input = user_args[UserArgs.INPUT.value]
        dest = user_args[UserArgs.OUTPUT.value]
        package_factory = packager.PackageFactory(packager.packages.CaptureOnePackage())

        for package in package_factory.locate_packages(source_input):
            jobs.append({
                JobValues.PACKAGE.value: package,
                JobValues.OUTPUT.value: dest,
                JobValues.SOURCE_PATH.value: source_input
            }
            )
        return jobs

    @staticmethod
    def new_job() -> typing.Type[worker.ProcessJob]:
        return PackageConverter

    @staticmethod
    def get_user_options() -> typing.List[tool_options.UserOption2]:
        return [
            tool_options.UserOptionCustomDataType(UserArgs.INPUT.value, tool_options.FolderData),
            tool_options.UserOptionCustomDataType(UserArgs.OUTPUT.value, tool_options.FolderData),
        ]

    @staticmethod
    def validate_args(**user_args):
        if not os.path.exists(user_args[UserArgs.INPUT.value]) or not os.path.isdir(user_args[UserArgs.INPUT.value]):
            raise ValueError("Invalid value in input ")

        if not os.path.exists(user_args[UserArgs.OUTPUT.value]) or not os.path.isdir(user_args[UserArgs.OUTPUT.value]):
            raise ValueError("Invalid value in output ")


class PackageConverter(ProcessJob):

    @contextmanager
    def log_config(self, logger):
        gui_logger = GuiLogHandler(self.log)
        try:
            logger.addHandler(gui_logger)
            yield
        finally:
            logger.removeHandler(gui_logger)

    def process(self, *args, **kwargs):
        my_logger = logging.getLogger(packager.__name__)
        my_logger.setLevel(logging.INFO)
        with self.log_config(my_logger):
            existing_package = kwargs[JobValues.PACKAGE.value]
            new_package_root = kwargs[JobValues.OUTPUT.value]
            source_path = kwargs[JobValues.SOURCE_PATH.value]
            package_id = existing_package.metadata['id']
            self.log(f"Converting {package_id} from {source_path} to a Hathi Trust Tiff package at {new_package_root}")
            package_factory = packager.PackageFactory(packager.packages.HathiTiff())
            package_factory.transform(existing_package, dest=new_package_root)
