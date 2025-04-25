from sqlalchemy import Integer, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func


from app.extensions import db

class Ticket(db.Model):
    __tablename__ = "tickets"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    ticket_title: Mapped[str] = mapped_column(String(255))
    requester_username: Mapped[str] = mapped_column(String(150))
    requester_fullname: Mapped[str] = mapped_column(String(35))
    department: Mapped[str] = mapped_column(String(20))
    anydesk: Mapped[str] = mapped_column(String(25))
    computer_name: Mapped[str] = mapped_column(String(35))
    creation_datetime: Mapped[DateTime] = mapped_column(DateTime, default=func.now(), nullable=False)
    user_glpi_id: Mapped[int]
    ticket_glpi_id: Mapped[int] = mapped_column(nullable=False)
    requester_ip: Mapped[str] = mapped_column(String(20))