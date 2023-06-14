from voucher.index import db


class Transaction(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.Text())
    amount = db.Column(db.Float())
    created_at = db.Column(db.DateTime())
    type = db.Column(db.String(10))
