from sqlalchemy import (
    Column,
    Integer,
    Text,
    text,
    DateTime
)

from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.db import db


class DetectionRecord(db.Model):
    __tablename__ = 'detection_record'
    __table_args__ = (
        {
            'mysql_engine': 'InnoDB',
            'mysql_charset': 'utf8',
            'mysql_collate': 'utf8_general_ci'
        }
    )

    id = Column(
        Integer,
        primary_key=True,
        autoincrement=True,
        nullable=False
    )
    detail = Column(Text, nullable=True)
    runtime = Column(Integer, nullable=True, default=None)
    created_at = Column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP")
    )
    updated_at = Column(
        DateTime,
        nullable=False,
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP")
    )

    def __repr__(self):
        return f'<DetectionRecord(id={self.id})>'


# todo: create a base class for schemas
class DetectionRecordSchema(SQLAlchemyAutoSchema):
    created_at = fields.DateTime('%Y-%m-%dT%H:%M:%S.000Z')  # javascript iso format
    updated_at = fields.DateTime('%Y-%m-%dT%H:%M:%S.000Z')
    # todo: maybe marshmallow can automatically load json string when dumping?

    class Meta:
        sqla_session = db.session
        model = DetectionRecord
        strict = True
        dump_only = ['id', 'created_at', 'updated_at']