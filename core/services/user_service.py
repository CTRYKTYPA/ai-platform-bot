from sqlalchemy import select
from core.models import User

async def get_or_create_user(session, telegram_id: int, username: str = None, full_name: str = None):
    """Fetch a user by telegram_id, or create them if not exists. Updates username/full_name if provided."""
    result = await session.execute(select(User).filter_by(telegram_id=telegram_id))
    user = result.scalars().first()
    if user:

        updated = False
        if username is not None and user.username != username:
            user.username = username
            updated = True
        if full_name is not None and user.full_name != full_name:
            user.full_name = full_name
            updated = True

    else:
        user = User(telegram_id=telegram_id, username=username, full_name=full_name)
        session.add(user)
    return user
