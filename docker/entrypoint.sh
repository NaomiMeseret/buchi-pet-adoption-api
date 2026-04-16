#!/bin/sh
set -e

python -c "from app.infrastructure.db import Base, engine; Base.metadata.create_all(bind=engine)"

exec "$@"
