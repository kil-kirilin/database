from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app) # Разрешить CORS для фронтенда

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/DT'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Определение модели данных для таблицы 'items'
class Item(db.Model):
    __tablename__ = 'items'
    # Используем id как Primary Key, auto-incrementing
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    # Поле 'number' может быть уникальным, если это номер позиции
    number = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    quantity = db.Column(db.String(100), nullable=False)
    monthlyConsumption = db.Column(db.String(100), nullable=False)
    yearlyConsumption = db.Column(db.String(100), nullable=False)
    monthlyPrice = db.Column(db.String(100), nullable=False)
    yearlyPrice = db.Column(db.String(100), nullable=False)
    note = db.Column(db.String(255), nullable=True) # Примечание может быть необязательным

    def to_dict(self):
        return {
            'number': self.number,
            'name': self.name,
            'quantity': self.quantity,
            'monthlyConsumption': self.monthlyConsumption,
            'yearlyConsumption': self.yearlyConsumption,
            'monthlyPrice': self.monthlyPrice,
            'yearlyPrice': self.yearlyPrice,
            'note': self.note
        }

# Маршрут для получения всех данных и добавления новой записи
@app.route('/api/data', methods=['GET', 'POST'])
def handle_items():
    if request.method == 'GET':
        items = Item.query.all()
        return jsonify([item.to_dict() for item in items])
    elif request.method == 'POST':
        data = request.get_json()
        if not data:
            return jsonify({"error": "Нет данных для добавления"}), 400

        # Проверка на наличие обязательных полей
        required_fields = ['number', 'name', 'quantity', 'monthlyConsumption',
                           'yearlyConsumption', 'monthlyPrice', 'yearlyPrice']
        for field in required_fields:
            if field not in data:
                return jsonify({"error": f"Отсутствует обязательное поле: {field}"}), 400

        # Создание нового объекта Item
        new_item = Item(
            number=data['number'],
            name=data['name'],
            quantity=data['quantity'],
            monthlyConsumption=data['monthlyConsumption'],
            yearlyConsumption=data['yearlyConsumption'],
            monthlyPrice=data['monthlyPrice'],
            yearlyPrice=data['yearlyPrice'],
            note=data.get('note', '') # Используем .get() для необязательного поля 'note'
        )

        try:
            db.session.add(new_item)
            db.session.commit()
            return jsonify({"message": "Элемент успешно добавлен", "item": new_item.to_dict()}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": f"Ошибка при добавлении элемента: {str(e)}"}), 500

# Маршрут для удаления записи по номеру
@app.route('/api/data/<string:item_number>', methods=['DELETE'])
def delete_item(item_number):
    # Ищем элемент по полю 'number', которое мы сделали уникальным
    item_to_delete = Item.query.filter_by(number=item_number).first()

    if not item_to_delete:
        return jsonify({"error": "Элемент не найден"}), 404

    try:
        db.session.delete(item_to_delete)
        db.session.commit()
        return jsonify({"message": f"Элемент №{item_number} успешно удален"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": f"Ошибка при удалении элемента: {str(e)}"}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)
