import sqlalchemy as sa
from gino import Gino

db = Gino()


class BlockedNumbers(db.Model):
    __tablename__ = 'phone_numbers'

    id = sa.Column(sa.Integer(), primary_key=True)
    phone_number = sa.Column(sa.String(15), unique=True)

    @classmethod
    async def check_if_number_is_blocked(cls, phone_number: str) -> bool:
        """Check if phone number is in the stop list"""
        if await BlockedNumbers.query.where(cls.phone_number == phone_number).gino.one_or_none():
            return True
        return False
