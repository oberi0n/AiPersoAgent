from __future__ import annotations

from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.models import Base


class Database:
    def __init__(self, database_url: str):
        self.engine = create_engine(database_url, future=True)
        self.session_factory = sessionmaker(bind=self.engine, class_=Session, expire_on_commit=False)

    def init_db(self) -> None:
        Base.metadata.create_all(self.engine)

    @contextmanager
    def session(self):
        session = self.session_factory()
        try:
            yield session
            session.commit()
        except Exception:
            session.rollback()
            raise
        finally:
            session.close()
