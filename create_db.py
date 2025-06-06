from app import create_app, db
from app.models import Book

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    sample_books = [
        Book(title="Harry Potter and the Sorcerer's Stone", author="J.K. Rowling", genre="Fantasy", year=1997),
        Book(title="To Kill a Mockingbird", author="Harper Lee", genre="Fiction", year=1960),
        Book(title="1984", author="George Orwell", genre="Dystopia", year=1949),
        Book(title="The Great Gatsby", author="F. Scott Fitzgerald", genre="Classic", year=1925),
    ]

    db.session.bulk_save_objects(sample_books)
    db.session.commit()

    print("Sample books inserted into the database.")
