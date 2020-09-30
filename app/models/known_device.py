from sqlalchemy import (
    Column,
    Integer,
    String,
    UniqueConstraint,
    text,
    DateTime
)
from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from app.db import db


class KnownDevice(db.Model):
    __tablename__ = 'known_device'
    __table_args__ = (
        UniqueConstraint('mac_addr'),
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
    mac_addr = Column(String(length=50), nullable=False)
    owner = Column(String(length=50), nullable=False)
    name = Column(String(length=200), nullable=True)
    vendor = Column(String(length=200), nullable=True)
    model = Column(String(length=200), nullable=True)
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
        return f'<KnownDevice(id={self.id}, mac_addr={self.mac_addr}, owner={self.owner}, name={self.name})>'


# todo: create a base class for schemas
class KnownDeviceSchema(SQLAlchemyAutoSchema):
    created_at = fields.DateTime('%Y-%m-%dT%H:%M:%S.000Z')  # javascript iso format
    updated_at = fields.DateTime('%Y-%m-%dT%H:%M:%S.000Z')

    class Meta:
        sqla_session = db.session
        model = KnownDevice
        strict = True
        dump_only = ['id', 'created_at', 'updated_at']


class KnownDeviceUpdateSchema(KnownDeviceSchema):
    mac_addr = fields.Str(required=False)
    owner = fields.Str(required=False)

