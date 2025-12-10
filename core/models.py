from datetime import datetime, date
from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    ForeignKey,
    DateTime,
    Date,
    Text,
    UniqueConstraint,
    BigInteger,
    Numeric,
)
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, unique=True, index=True)
    username = Column(String(32))
    full_name = Column(String(100))

    # Статус пользователя: free / paid / donor
    status = Column(String(20), default="free", nullable=False)

    notifications_enabled = Column(Boolean, default=True)
    wants_community = Column(Boolean, default=False)

    subscriptions = relationship(
        "Subscription", back_populates="user", cascade="all, delete-orphan"
        )
    progress_list = relationship(
        "UserProgramProgress", back_populates="user", cascade="all, delete-orphan"
        )
    meeting_notifications = relationship(
        "UserMeetingNotification", back_populates="user", cascade="all, delete-orphan"
        )
    qa_logs = relationship(
        "QALog", back_populates="user", cascade="all, delete-orphan"
        )
    donations = relationship(
        "Donation", back_populates="user", cascade="all, delete-orphan"
        )


class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    plan = Column(String(50))          # тип подписки (monthly / trial и т.п.)
    start_date = Column(Date)
    end_date = Column(Date)
    activated_by = Column(String(100)) # кто активировал (админ)
    comment = Column(Text)

    user = relationship("User", back_populates="subscriptions")


class Category(Base):
    __tablename__ = "categories"

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    description = Column(Text)

    materials = relationship(
        "Material", back_populates="category", cascade="all, delete-orphan"
        )


class Material(Base):
    __tablename__ = "materials"

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    content = Column(Text)
    content_type = Column(String(20))  # text / link / html и т.п.

    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Category", back_populates="materials")

    # Уровень доступа к материалу: free / paid (в будущем можно добавить donor)
    access_level = Column(String(20), default="free", nullable=False)

    # Если указана дата — материал используется как “Материал дня” на эту дату
    scheduled_date = Column(Date)


class Template(Base):
    __tablename__ = "templates"

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    content = Column(Text)


class Program(Base):
    __tablename__ = "programs"

    id = Column(Integer, primary_key=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)

    # Уровень доступа к программе: free / paid (в будущем можно добавить donor)
    access_level = Column(String(20), default="free", nullable=False)

    steps = relationship(
        "ProgramStep", back_populates="program", cascade="all, delete-orphan"
        )
    progresses = relationship(
        "UserProgramProgress", back_populates="program", cascade="all, delete-orphan"
        )


class ProgramStep(Base):
    __tablename__ = "program_steps"

    id = Column(Integer, primary_key=True)
    program_id = Column(Integer, ForeignKey("programs.id", ondelete="CASCADE"))
    step_number = Column(Integer)
    content = Column(Text)

    program = relationship("Program", back_populates="steps")

    __table_args__ = (
        UniqueConstraint("program_id", "step_number", name="uq_program_step"),
    )


class UserProgramProgress(Base):
    __tablename__ = "user_program_progress"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    program_id = Column(Integer, ForeignKey("programs.id", ondelete="CASCADE"))

    current_step = Column(Integer, default=0)
    is_completed = Column(Boolean, default=False)
    started_at = Column(DateTime)
    completed_at = Column(DateTime)

    user = relationship("User", back_populates="progress_list")
    program = relationship("Program", back_populates="progresses")

    __table_args__ = (
        UniqueConstraint("user_id", "program_id", name="uq_user_program"),
    )


class Meeting(Base):
    __tablename__ = "meetings"

    id = Column(Integer, primary_key=True)
    topic = Column(String(200), nullable=False)
    scheduled_at = Column(DateTime, nullable=False)
    link = Column(String(300))


    is_premium = Column(Boolean, default=False)

    notifications = relationship(
        "UserMeetingNotification", back_populates="meeting", cascade="all, delete-orphan"
        )


class UserMeetingNotification(Base):
    __tablename__ = "user_meeting_notifications"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))
    meeting_id = Column(Integer, ForeignKey("meetings.id", ondelete="CASCADE"))

    user = relationship("User", back_populates="meeting_notifications")
    meeting = relationship("Meeting", back_populates="notifications")

    __table_args__ = (
        UniqueConstraint("user_id", "meeting_id", name="uq_user_meeting_notif"),
    )


class QALog(Base):
    __tablename__ = "qa_log"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"))
    question = Column(Text)
    answer = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="qa_logs")


class Donation(Base):
    """
    Задел под систему добровольных пожертвований.
    """
    __tablename__ = "donations"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"))

    amount = Column(Numeric(10, 2))          # сумма, например, в рублях
    currency = Column(String(10), default="RUB")
    created_at = Column(DateTime, default=datetime.utcnow)
    comment = Column(Text)
    provider = Column(String(50))            # платежный провайдер / способ

    user = relationship("User", back_populates="donations")
