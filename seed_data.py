from app import create_app, db
from app.models import Book
from faker import Faker
import random
import os

print("DB_USER:", os.getenv('DB_USER'))
print("DB_PASSWORD:", os.getenv('DB_PASSWORD'))
print("DB_HOST:", os.getenv('DB_HOST'))
print("DB_PORT:", os.getenv('DB_PORT'))
print("DB_NAME:", os.getenv('DB_NAME'))

app = create_app()
print("App DB URI:", app.config['SQLALCHEMY_DATABASE_URI'])

faker = Faker()
genres = ["Fiction", "Fantasy", "Mystery", "Sci-Fi", "Biography", "History", "Romance", "Horror", "Philosophy"]

with app.app_context():
    db.drop_all()
    db.create_all()

    books = []
    for _ in range(1000):
        book = Book(
            title=faker.sentence(nb_words=4),
            author=faker.name(),
            genre=random.choice(genres),
            year=random.randint(1900, 2024)
        )
        books.append(book)

    db.session.bulk_save_objects(books)
    db.session.commit()

    print("1000 fake books inserted into database.")
