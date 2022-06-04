from datetime import datetime

from sqlalchemy import Column, String, DateTime, Integer, Text

from models.database import Base


class Post(Base):
    __tablename__ = 'posts'

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(256), nullable=False)
    text = Column(Text)
    created_at = Column(DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return (
            f'<{self.__class__.__name__}('
            f'id={self.id}, '
            f'username={self.title}, '
            f')>'
        )
