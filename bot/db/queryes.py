from bot.loader import session
from bot.db.models import User


async def verification(id: int) -> bool:
    user = session.query(User).filter(User.id == id).first()
    if user:
        return True
    return False
