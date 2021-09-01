#
# @Author: Bhaskar S
# @Blog:   https://www.polarsparc.com
# @Date:   01 Sep 2021
#

from sqlalchemy import Column, String
from werkzeug.security import generate_password_hash, check_password_hash
from config.config import Base, engine, session

class User(Base):
    __tablename__ = 'user_tbl'
    email_id = Column(String(64), primary_key=True)
    password_hash = Column(String(64))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {0}>'.format(self.email_id)

    @staticmethod
    def register(email, password):
        user = User(email_id=email)
        user.set_password(password)
        session.add(user)
        session.commit()
        return user

    @staticmethod
    def query_by_email(email):
        return session.query(User).filter(User.email_id == email).first()

Base.metadata.create_all(engine, checkfirst=True)
