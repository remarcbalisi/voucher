from marshmallow import post_load

from .transaction import Transaction, TransactionSchema
from .transaction_type import TransactionType


class Credit(Transaction):
    def __init__(self, description, amount):
        super(Credit, self).__init__(description, amount, TransactionType.ADD_CREDITS.__str__())

    def __repr__(self):
        return '<Income(name={self.description!r})>'.format(self=self)


class CreditSchema(TransactionSchema):
    @post_load
    def make_income(self, data, **kwargs):
        return Credit(**data)
