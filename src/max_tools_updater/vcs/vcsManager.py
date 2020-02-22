from lib.sdk.singleton import Singleton


class VCSManager(object):
    __metaclass__ = Singleton

    packagesToUpdate = None

    def __init__(self):
        self.packagesToUpdate = list()
