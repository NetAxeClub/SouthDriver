import logging


log = logging.getLogger(__name__)


class NetpalmDriver:
    """ NetPalmDriver is the base class for all NetPalm drivers. """

    driver_name = None

    def __init__(self, **kwargs):
        log.info(f"netpalm service: invoking")

    def connect(self):
        """connect to the device"""
        raise NotImplementedError

    def sendcommand(self, session, command):
        """send a command to the device"""
        raise NotImplementedError

    def config(self, sesh, config):
        """send a config to the device"""
        raise NotImplementedError

    def logout(self, session):
        """logout of the device"""
        raise NotImplementedError