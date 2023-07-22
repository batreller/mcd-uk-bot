from database.connector import session
from database.models import User


async def get_user(message) -> User:
    user_id = message.from_user.id
    user = session.query(User).filter_by(id=user_id).first()
    if not user:
        username = message.from_user.username
        first_name = message.from_user.first_name
        last_name = message.from_user.last_name
        user = User(id=user_id, username=username, first_name=first_name, last_name=last_name, language='no')
        session.add(user)
        session.commit()
    return user
