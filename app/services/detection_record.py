import json
from app.services.base import BaseService
from app.models.detection_record import DetectionRecord as DetectionRecordModel, DetectionRecordSchema
from app.models.known_device import KnownDevice as KnownDeviceModel, KnownDeviceSchema
from app.services.known_device import KnownDevice as KnownDeviceService


class DetectionRecord(BaseService):
    model = DetectionRecordModel
    know_device_service = KnownDeviceService()
    detection_record_schema = DetectionRecordSchema()
    know_device_schema = KnownDeviceSchema()
    color_set = ['#206a5d', '#81b214', '#ffcc29', '#f58634', '#4b778d']

    def get_detection_records(self):
        records = self.select_all()
        dumped_records = self.detection_record_schema.dump(records, many=True)
        macs_detected = set()  # set of mac address string, this way all elements in there are unique

        for dumped_record in dumped_records:
            try:
                dumped_record['detail'] = json.loads(dumped_record['detail'])
            except:
                print('Error in get_detection_records: cannot parse json')
                dumped_record['detail'] = []

        for dumped_record in dumped_records:
            for device in dumped_record['detail']:
                macs_detected.add(device.get('mac'))  # may contain None

        macs_detected = [mac for mac in macs_detected if mac]  # Filter out empty values

        all_known_devices = self.know_device_service.select_all()

        owners = []
        for known_device in all_known_devices:
            new_owner = {
                'owner': known_device.owner,
                'devices': []
            }
            for owner in owners:
                if known_device.owner == owner['owner']:
                    owner['devices'].append(self.know_device_schema.dump(known_device))
                    new_owner = None
            if new_owner is not None:
                new_owner['devices'].append(self.know_device_schema.dump(known_device))
                owners.append(new_owner)

        for index, owner in enumerate(owners):
            idx = index % 5
            owner['color'] = self.color_set[idx]

        known_devices_detected = [device for device in all_known_devices if device.mac_addr in macs_detected]
        known_devices_detected = self.know_device_schema.dump(known_devices_detected, many=True)

        result = []
        for dumped_record in dumped_records:
            owner_device_rec = []
            devices = []
            # todo: switch to client side rendering, jinja is really not great at this
            for device in dumped_record['detail']:
                mac = device.get('mac')
                devices.append({
                    # this is a dict with the dump result of know_device_schema, and the ip from detection_record
                    **next(
                        (known_device for known_device in known_devices_detected if known_device['mac_addr'] == mac),
                        self.know_device_schema.dump(KnownDeviceModel())
                        # if device does not belong to known_devices_detected, create a new empty KnownDeviceModel obj
                        # and dump
                    ),
                    'ip': device.get('ip')
                })
            for owner in owners:
                for device in owner['devices']:
                    if len([rec for rec in dumped_record['detail'] if rec['mac'] == device['mac_addr']]) > 0:
                        owner_device_rec.append(owner['color'])
                    else:
                        owner_device_rec.append('#fff')
            dumped_record['owner_device_rec'] = owner_device_rec
            dumped_record['detail'] = devices
            result.append(dumped_record)

        return {
            'ownerships': owners,
            'detection_records': result
        }
