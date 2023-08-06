from datetime import datetime, timezone
from uuid import uuid4 as gen_uuid


def utcnow():
    return datetime.utcnow().replace(tzinfo=timezone.utc)


def uuid4():
    return str(gen_uuid())
