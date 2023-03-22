import uuid
import ormar
from datetime import datetime
import bcrypt

from src.database import metadata, database


class User(ormar.Model):
    class Meta:
        metadata = metadata
        database = database
        tablename = "users"

    id: uuid.UUID = ormar.UUID(primary_key=True, default=uuid.uuid4)
    username: str = ormar.String(unique=True, max_length=255)
    email: str = ormar.String(index=True, unique=True, max_length=255)
    hashed_password: str = ormar.String(max_length=255)
    is_active: bool = ormar.Boolean(default=False, nullable=False)
    is_superuser: bool = ormar.Boolean(default=False, nullable=False)
    created_at: datetime = ormar.DateTime(default=datetime.utcnow)

    @property
    def password(self):
        raise AttributeError('La password non può essere letta')

    @password.setter
    def password(self, plaintext_password):
        self.hashed_password = bcrypt.hashpw(plaintext_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, plaintext_password):
        return bcrypt.checkpw(plaintext_password.encode('utf-8'), self.hashed_password.encode('utf-8'))

    def check_active(self):
        if self.is_active:
            return True
        else:
            return False


class APIKey(ormar.Model):
    class Meta:
        metadata = metadata
        database = database
        tablename = "apikey"

    apikey: str = ormar.String(primary_key=True, max_length=22)
    id_user = ormar.UUID(default=uuid.uuid4)
    created_at: datetime = ormar.DateTime(default=datetime.utcnow)
