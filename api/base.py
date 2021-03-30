from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import registry

db = SQLAlchemy()
mapper_registry = registry()
base = mapper_registry.generate_base()