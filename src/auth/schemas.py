import uuid
import ormar
from datetime import datetime

from src.database import metadata, database


class UserModel(ormar.Model):
    class Meta():
        metadata = metadata
        database = database
        tablename = "users"

    id: uuid.UUID = ormar.UUID(primary_key=True, default=uuid.uuid4)
    email: str = ormar.String(index=True, unique=True, max_length=255)
    hashed_password: str = ormar.String(max_length=255)
    is_active: bool = ormar.Boolean(default=True)
    is_superuser: bool = ormar.Boolean(default=False)
    created_at: datetime = ormar.DateTime(default=datetime.utcnow)
    updated_at: datetime = ormar.DateTime(default=datetime.utcnow)
