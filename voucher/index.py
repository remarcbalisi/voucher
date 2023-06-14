import configparser
import os
from flask import Flask, jsonify, request, render_template, send_from_directory
from flask_pymongo import PyMongo


app = Flask(__name__)
mongo = PyMongo(app)

config = configparser.ConfigParser()
config.read(os.path.abspath(os.path.join(".ini")))
app.config['MONGO_URI'] = config['PROD']['DB_URI']


@app.route('/')
def index():
    print('Request for index page received')
    return render_template('index.html')


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


# @app.route('/credits')
# def get_credits():
#     schema = CreditSchema(many=True)
#     total_credits = db.session.execute(db.select(Transaction)).scalars().all()
#     print(total_credits)
#     incomes = schema.dump(
#         filter(lambda t: t.type == TransactionType.ADD_CREDITS, transactions)
#     )
#     return jsonify(total_credits)
#
#
# @app.route('/add-credits', methods=['POST'])
# def add_credits():
#     # credit = CreditSchema().load(request.get_json())
#     # print(type(request.get_json()))
#     income = Transaction(**request.get_json())
#     db.session.add(income)
#     db.session.commit()
#     # transactions.append(income)
#     return jsonify({"message": "Success"}), 201
#
#
# @app.route('/expenses')
# def get_expenses():
#     schema = ExpenseSchema(many=True)
#     expenses = schema.dump(
#         filter(lambda t: t.type == TransactionType.EXPENSE, transactions)
#     )
#     return jsonify(expenses)
#
#
# @app.route('/expenses', methods=['POST'])
# def add_expense():
#     expense = ExpenseSchema().load(request.get_json())
#     transactions.append(expense)
#     return "", 204


if __name__ == "__main__":
    app.run()
