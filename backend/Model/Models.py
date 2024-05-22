from Database.db import db
from datetime import datetime
from sqlalchemy.orm import relationship


class AccountModel(db.Model):
    __tablename__ = 'account'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, nullable=False)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    cameras = db.relationship('CameraModel', back_populates='owner',
                              lazy='dynamic')

    def __str__(self) -> str:
        return str(self.json())

    def __repr__(self) -> str:
        return f"<Account{self.id}email={self.email}username={self.username})>"

    def json(self):
        return {
            'id': self.id,
            'email': self.email,
            'username': self.username,
            'password': self.password,
        }


class CameraModel(db.Model):
    __tablename__ = 'cameras'
    id = db.Column(db.Integer, primary_key=True)
    # Foreign Key Relationship
    owner_id = db.Column(db.Integer, db.ForeignKey('account.id'),
                         nullable=False)
    owner = relationship("AccountModel", back_populates="cameras")
    name = db.Column(db.String(100), nullable=False)
    location = db.Column(db.String(255))
    ip_address = db.Column(db.String(15))
    port = db.Column(db.Integer)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return (
            f"Camera(id={self.id}, name='{self.name}'"
            f"location='{self.location}',"
            f" IP='{self.ip_address}', owner_id={self.owner_id})"
        )
