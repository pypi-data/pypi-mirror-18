from ereuse_devicehub.resources.device.schema import Device
from ereuse_devicehub.resources.device.settings import DeviceSubSettings


class Computer(Device):
    type = {
        'type': 'string',
        'allowed': {'Desktop', 'Laptop', 'Netbook', 'Server', 'Microtower'}
    }
    forceCreation = {
        'type': 'boolean',
        'default': False
    }


class ComputerSettings(DeviceSubSettings):
    _schema = Computer
    etag_ignore_fields = DeviceSubSettings.etag_ignore_fields + ['forceCreation']
