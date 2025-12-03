from app import app, db, Item # Импортируем app и db из вашего файла app.py

def create_db_and_tables():
    with app.app_context():
        # Создаем все таблицы, определенные в моделях SQLAlchemy
        db.create_all()
        print("База данных и таблицы созданы.")

        # Проверяем, пуста ли таблица 'items', чтобы избежать дублирования при повторном запуске
        if Item.query.first() is None:
            # Данные для заполнения таблицы 'items'
            initial_data = [
                {
                    "number": "1",
                    "name": "Бумага офисная А4",
                    "quantity": "10 пачек",
                    "monthlyConsumption": "2 пачки",
                    "yearlyConsumption": "24 пачки",
                    "monthlyPrice": "800",
                    "yearlyPrice": "9 600",
                    "note": "Белая, 80 г/м²"
                },
                {
                    "number": "2",
                    "name": "Картридж для принтера HP 85A",
                    "quantity": "5 шт",
                    "monthlyConsumption": "0.3 шт",
                    "yearlyConsumption": "4 шт",
                    "monthlyPrice": "1 200",
                    "yearlyPrice": "14 400",
                    "note": "Оригинальный"
                },
                {
                    "number": "3",
                    "name": "Ручка шариковая синяя",
                    "quantity": "100 шт",
                    "monthlyConsumption": "15 шт",
                    "yearlyConsumption": "180 шт",
                    "monthlyPrice": "450",
                    "yearlyPrice": "5 400",
                    "note": "Офисные"
                },
                {
                    "number": "4",
                    "name": "Кофе молотый",
                    "quantity": "3 кг",
                    "monthlyConsumption": "1.5 кг",
                    "yearlyConsumption": "18 кг",
                    "monthlyPrice": "2 500",
                    "yearlyPrice": "30 000",
                    "note": "Jacobs Monarch"
                },
                {
                    "number": "5",
                    "name": "Бумага для факса",
                    "quantity": "8 рулонов",
                    "monthlyConsumption": "1 рулон",
                    "yearlyConsumption": "12 рулонов",
                    "monthlyPrice": "600",
                    "yearlyPrice": "7 200",
                    "note": "57мм х 30м"
                },
                {
                    "number": "6",
                    "name": "Маркеры перманентные",
                    "quantity": "20 шт",
                    "monthlyConsumption": "3 шт",
                    "yearlyConsumption": "36 шт",
                    "monthlyPrice": "900",
                    "yearlyPrice": "10 800",
                    "note": "Черные, тонкие"
                },
                {
                    "number": "7",
                    "name": "Скотч упаковочный",
                    "quantity": "12 шт",
                    "monthlyConsumption": "2 шт",
                    "yearlyConsumption": "24 шт",
                    "monthlyPrice": "480",
                    "yearlyPrice": "5 760",
                    "note": "45мм х 50м"
                },
                {
                    "number": "8",
                    "name": "Блокноты А5",
                    "quantity": "25 шт",
                    "monthlyConsumption": "4 шт",
                    "yearlyConsumption": "48 шт",
                    "monthlyPrice": "800",
                    "yearlyPrice": "9 600",
                    "note": "В клетку, 80 листов"
                },
                {
                    "number": "9",
                    "name": "Папки-скоросшиватели",
                    "quantity": "30 шт",
                    "monthlyConsumption": "5 шт",
                    "yearlyConsumption": "60 шт",
                    "monthlyPrice": "750",
                    "yearlyPrice": "9 000",
                    "note": "Пластиковые, А4"
                },
                {
                    "number": "10",
                    "name": "Тонер для копировального аппарата",
                    "quantity": "4 шт",
                    "monthlyConsumption": "0.5 шт",
                    "yearlyConsumption": "6 шт",
                    "monthlyPrice": "3 500",
                    "yearlyPrice": "42 000",
                    "note": "Canon 045"
                }
            ]

            for data in initial_data:
                item = Item(**data)
                db.session.add(item)
            db.session.commit()
            print("Данные успешно добавлены в таблицу 'items'.")
        else:
            print("Таблица 'items' уже содержит данные. Пропускаем добавление.")

if __name__ == '__main__':
    # Сначала убедитесь, что база данных 'database-light' существует в PostgreSQL.
    # Вы можете создать ее вручную через psql или pgAdmin:
    # CREATE DATABASE "database-light";
    # CREATE USER postgres WITH PASSWORD 'postgres';
    # GRANT ALL PRIVILEGES ON DATABASE "database-light" TO postgres;

    create_db_and_tables()