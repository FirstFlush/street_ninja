from abc import ABC
import logging


logger = logging.getLogger(__name__)


class BaseResponseBuilder(ABC):

    def __init__(self):
        ...
