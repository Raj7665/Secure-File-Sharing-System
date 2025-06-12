from app import db
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    files = db.relationship('File', backref='owner', lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}')"

class File(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(255), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    upload_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    is_shared = db.Column(db.Boolean, default=False)
    share_link = db.Column(db.String(255), unique=True, nullable=True)

    # Many-to-many relationship for shared files
    shared_with = db.relationship(
        'User', secondary='shared_files',
        primaryjoin="File.id == SharedFile.file_id",
        secondaryjoin="User.id == SharedFile.user_id",
        backref=db.backref('can_access_files', lazy='dynamic'),
        lazy='dynamic'
    )

    def __repr__(self):
        return f"File('{self.filename}', '{self.upload_date}')"

class SharedFile(db.Model):
    __tablename__ = 'shared_files'
    file_id = db.Column(db.Integer, db.ForeignKey('file.id'), primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), primary_key=True)
    shared_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
