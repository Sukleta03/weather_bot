from bot.loader import session
from db.models import User


async def verification(user_id: int) -> bool:
    user = session.query(User).filter(User.id == user_id).first()
    if user:
        return True
    return False
