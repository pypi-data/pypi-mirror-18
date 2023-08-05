from ereuse_devicehub.resources.event.device.domain import DeviceEventDomain
from ereuse_devicehub.resources.event.device.settings import EventWithDevices, EventSubSettingsMultipleDevices
from ereuse_devicehub.resources.resource import Resource

"""
    Registers the generic types for the events.

    This module creates as many Schema (extending from EventWithDevices) and Settings (extending from
    EventSubSettingsMultipleDevices) as generic types are.
"""

for (generic_type, settings) in DeviceEventDomain.GENERIC_TYPES.items():
    Resource.create(generic_type, EventWithDevices, {}, EventSubSettingsMultipleDevices, settings)
