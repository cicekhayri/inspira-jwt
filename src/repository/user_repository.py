from sqlalchemy.exc import SQLAlchemyError

from database import db_session
from src.model.user import User


class UserRepository:

    def get_all_user(self):
        return db_session.query(User).all()

    def get_user_by_id(self, user_id: int) -> User:
        return db_session.query(User).filter_by(id=user_id).first()

    def get_user_by_email(self, email: str) -> User:
        return db_session.query(User).filter_by(email=email).first()

    def create_user(self, user: User) -> bool:
        try:
            db_session.add(user)
            db_session.commit()
            return True
        except SQLAlchemyError as e:
            db_session.rollback()
            print(f"Error creating user: {e}")
            return False