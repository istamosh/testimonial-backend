from typing import TYPE_CHECKING, List
from app.extensions import db, bcrypt
from sqlalchemy.orm import Mapped, mapped_column, relationship

if TYPE_CHECKING:
    from app.models.preserved_testimonial import PreservedTestimonial

class User(db.Model):
    """User model for authentication and account management."""
    
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(db.String(80), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(db.String(120), nullable=False)
    
    # Relationships
    preserved_testimonials: Mapped[List["PreservedTestimonial"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
        cascade_backrefs=False
    )

    def set_password(self, password: str) -> None:
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def check_password(self, password: str) -> bool:
        return bcrypt.check_password_hash(self.password, password)

    def __repr__(self) -> str:
        return f'<User {self.username}>'
