from datetime import datetime

from sqlalchemy.orm import Mapped, mapped_column, registry

table_registry = registry()


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(init=False, primary_key=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]
    name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True)
    phone: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(
        init=False, default=datetime.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, default=datetime.now()
    )
