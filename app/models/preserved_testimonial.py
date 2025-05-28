from datetime import datetime, timezone
from typing import TYPE_CHECKING
from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid

if TYPE_CHECKING:
    from app.models.user import User

class PreservedTestimonial(db.Model):
    """Model for storing preserved testimonial information."""
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(120), nullable=False)
    access_uuid: Mapped[str] = mapped_column(
        db.String(36), 
        nullable=False, 
        default=lambda: str(uuid.uuid4()), 
        unique=True, 
        index=True
    )
    created_at: Mapped[datetime] = mapped_column(
        default=datetime.now(timezone.utc), 
        nullable=False
    )
    user_id: Mapped[int] = mapped_column(
        db.ForeignKey("user.id", ondelete="CASCADE"), 
        nullable=False
    )
    
    # Relationship
    user: Mapped["User"] = relationship(
        back_populates="preserved_testimonials",
        cascade_backrefs=False
    )

    def __repr__(self) -> str:
        return f'<PreservedTestimonial {self.name}>'