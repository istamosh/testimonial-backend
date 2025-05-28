from datetime import datetime, timezone
from typing import Optional
from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column
import uuid
from sqlalchemy import Enum

class Testimonial(db.Model):
    """Model for storing testimonials from users."""
    
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(db.String(120), nullable=False)
    photo_url: Mapped[Optional[str]] = mapped_column(db.String(255), nullable=True)
    testimonial: Mapped[str] = mapped_column(db.Text, nullable=False)
    rating: Mapped[int] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(
        Enum('draft', 'published', name='testimonial_status'),
        nullable=False, default='draft'
    )
    date_posted: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    created_from_invite: Mapped[str] = mapped_column(
        db.String(36),
        nullable=False,
        default=lambda: str(uuid.uuid4())
    )
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc))
    filled_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    def __repr__(self) -> str:
        return f'<Testimonial {self.name} - {self.rating}>'
