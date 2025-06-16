from datetime import datetime, timezone
from typing import Optional
from app.extensions import db
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Enum

class Testimonial(db.Model):
    """Model for storing testimonials from users."""
    
    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(db.String(60), nullable=False)
    last_name: Mapped[str] = mapped_column(db.String(60), nullable=False)
    role_company: Mapped[Optional[str]] = mapped_column(db.String(120), nullable=True)
    testimonial: Mapped[str] = mapped_column(db.Text, nullable=False)
    censor_first_name: Mapped[bool] = mapped_column(db.Boolean, default=False, nullable=False)
    censor_last_name: Mapped[bool] = mapped_column(db.Boolean, default=False, nullable=False)
    consent_given: Mapped[bool] = mapped_column(db.Boolean, default=False, nullable=False)
    status: Mapped[str] = mapped_column(
        Enum('PENDING', 'APPROVED', 'REJECTED', name='testimonial_status'),
        nullable=False, default='PENDING'
    )
    created_at: Mapped[datetime] = mapped_column(default=datetime.now(timezone.utc), nullable=False)
    approved_at: Mapped[Optional[datetime]] = mapped_column(nullable=True)

    def __repr__(self) -> str:
        return f'<Testimonial {self.first_name} {self.last_name}>'
