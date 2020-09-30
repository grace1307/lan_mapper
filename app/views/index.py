from flask import Blueprint, jsonify, make_response, abort, request
from jinja2 import Environment, FileSystemLoader
from app.services.detection_record import DetectionRecord as DetectionRecordService
from app.services.known_device import KnownDevice as KnownDeviceService
from app.models.known_device import KnownDeviceSchema, KnownDeviceUpdateSchema
from app.models.detection_record import DetectionRecordSchema

app = Blueprint('index', __name__)

file_env = Environment(loader=FileSystemLoader('html'))
report_template = file_env.get_template('report.html')


@app.route('/', methods=['GET'])
def index():
    return make_response(jsonify({'is_running': True}), 200)


@app.route('/api/known_devices/<id>', methods=['GET'])
def get_known_device(id):
    if not id:
        return abort(400)

    id = int(id)
    result = KnownDeviceService().select_one(id=id)

    if result is None:
        return abort(404)

    known_device_schema = KnownDeviceSchema()

    return make_response(jsonify(known_device_schema.dump(result)), 200)


@app.route('/api/known_devices', methods=['GET'])
def get_known_devices():
    known_device_schema = KnownDeviceSchema()
    result = KnownDeviceService().select_all()

    return make_response(
        jsonify(
            known_device_schema.dump(result, many=True)
        ),
        200
    )


@app.route('/api/known_devices', methods=['POST'])
def add_known_device():
    known_device_schema = KnownDeviceSchema()

    # validation error will be caught by app.index.handle_marshmallow_validation
    content = known_device_schema.load(request.get_json())

    known_device_service = KnownDeviceService()
    result = known_device_service.add_one(**content)

    return make_response(jsonify(known_device_schema.dump(result)), 200)


@app.route('/api/known_devices/<id>', methods=['PATCH'])
def update_known_device(id):
    known_device_update_schema = KnownDeviceUpdateSchema()

    # validation error will be caught by app.index.handle_marshmallow_validation
    content = known_device_update_schema.load(request.get_json())

    known_device_service = KnownDeviceService()

    record = known_device_service.select_one(id)

    if record is None:
        return abort(404)

    result = known_device_service.update_one(id, updated=content)

    return make_response(jsonify(known_device_update_schema.dump(result)), 200)


@app.route('/api/known_devices/<id>', methods=['DELETE'])
def delete_known_device(id):
    known_device_service = KnownDeviceService()
    record = known_device_service.select_one(id)

    if record is None:
        return abort(404)

    known_device_service.delete_one(id)

    return make_response(jsonify(None), 204)


# todo: create R/U/D for detection_records
@app.route('/api/detection_record', methods=['POST'])
def add_detection_record():
    detection_record_schema = DetectionRecordSchema()
    content = detection_record_schema.load(request.get_json())

    detection_record_service = DetectionRecordService()
    result = detection_record_service.add_one(**content)

    return make_response(jsonify(detection_record_schema.dump(result)), 200)


@app.route('/view/report', methods=['GET'])
def view_report():
    detection_record_service = DetectionRecordService()
    result = detection_record_service.get_detection_records()

    return make_response(report_template.render(data=result), 200)
