from typing import List
from app.extensions import db, bcrypt
from sqlalchemy.orm import Mapped, mapped_column

class User(db.Model):
    """User model for authentication and account management."""
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(db.String(80), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(db.String(120), nullable=False)

    def set_password(self, password: str) -> None:
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password: str) -> bool:
        return bcrypt.check_password_hash(self.password, password)

    def __repr__(self) -> str:
        return f'<User {self.username}>'
