from app.services.base import BaseService
from app.models.known_device import KnownDevice as KnownDeviceModel


class KnownDevice(BaseService):
    model = KnownDeviceModel
