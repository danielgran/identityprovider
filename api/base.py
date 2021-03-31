from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import registry

import redis

redis_cache = redis.Redis()

db = SQLAlchemy()


mapper_registry = registry()
base = mapper_registry.generate_base()