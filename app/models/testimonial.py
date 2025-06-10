from datetime import datetime, timezone
from typing import Optional
from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Enum

class Testimonial(db.Model):
    """Model for storing testimonials from users."""
    
    id: Mapped[int] = mapped_column(primary_key=True)
    nameOrEmail: Mapped[str] = mapped_column(db.String(120), nullable=False)
    linkedin_url: Mapped[str] = mapped_column(db.String(255), nullable=False)
    testimonial: Mapped[str] = mapped_column(db.Text, nullable=False)
    status: Mapped[str] = mapped_column(
        Enum('PENDING', 'APPROVED', name='testimonial_status'),
        nullable=False, default='PENDING'
    )
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc), nullable=False)
    approved_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    def __repr__(self) -> str:
        return f'<Testimonial {self.nameOrEmail}>'
