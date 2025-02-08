from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from bot.database.schemas.base import Base

class AdminSchema(Base):
    __tablename__ = "admins"
    
    id: Mapped[Integer] = mapped_column(Integer, primary_key=True)
    username: Mapped[String] = mapped_column(String, nullable=False)    