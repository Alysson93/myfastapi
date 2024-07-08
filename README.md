## lint
isort .
blue .

## test
pytest

## run
python src/main.py

## alembic
alembic init
alembic revision --autogenerate -m "migration name"
alembic upgrade head