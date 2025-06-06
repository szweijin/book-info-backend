from flask import Blueprint, request, jsonify
from app.models import Book
from flasgger import swag_from
from app.db_utils import measure_query_time, explain_query

bp = Blueprint('books', __name__, url_prefix='/books')

@bp.route('', methods=['GET'])
@swag_from({
    'tags': ['Books'],
    'parameters': [
        {'name': 'title', 'in': 'query', 'type': 'string', 'required': False, 'description': 'Book title to search'},
        {'name': 'author', 'in': 'query', 'type': 'string', 'required': False, 'description': 'Author name to search'},
        {'name': 'genre', 'in': 'query', 'type': 'string', 'required': False, 'description': 'Genre to search'},
        {'name': 'page', 'in': 'query', 'type': 'integer', 'required': False, 'default': 1, 'description': 'Page number'},
        {'name': 'size', 'in': 'query', 'type': 'integer', 'required': False, 'default': 10, 'description': 'Page size'},
        {'name': 'sort_by', 'in': 'query', 'type': 'string', 'required': False, 'default': 'id', 'description': 'Sort by field'},
        {'name': 'order', 'in': 'query', 'type': 'string', 'required': False, 'default': 'asc', 'description': 'Sort order: asc or desc'}
    ],
    'responses': {
        200: {
            'description': 'List of books',
            'schema': {
                'type': 'object',
                'properties': {
                    'total': {'type': 'integer'},
                    'page': {'type': 'integer'},
                    'size': {'type': 'integer'},
                    'books': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'integer'},
                                'title': {'type': 'string'},
                                'author': {'type': 'string'},
                                'genre': {'type': 'string'},
                                'year': {'type': 'integer'},
                            }
                        }
                    }
                }
            }
        }
    }
})
@measure_query_time
def get_books():
    title = request.args.get('title', '')
    author = request.args.get('author', '')
    genre = request.args.get('genre', '')

    try:
        page = int(request.args.get('page', 1))
        if page < 1:
            page = 1
    except (ValueError, TypeError):
        page = 1

    try:
        size = int(request.args.get('size', 10))
        if size < 1 or size > 100:
            size = 10
    except (ValueError, TypeError):
        size = 10

    sort_by = request.args.get('sort_by', 'id')
    order = request.args.get('order', 'asc').lower()

    query = Book.query

    if title:
        query = query.filter(Book.title.ilike(f'%{title}%'))
    if author:
        query = query.filter(Book.author.ilike(f'%{author}%'))
    if genre:
        query = query.filter(Book.genre.ilike(f'%{genre}%'))

    if sort_by not in ['id', 'title', 'author', 'genre', 'year']:
        sort_by = 'id'

    sort_col = getattr(Book, sort_by)
    if order == 'desc':
        sort_col = sort_col.desc()
    else:
        sort_col = sort_col.asc()

    query = query.order_by(sort_col)

    total = query.count()

    sql = str(query.statement.compile(compile_kwargs={"literal_binds": True}))

    explain_query(sql)

    books = query.offset((page - 1) * size).limit(size).all()

    return jsonify({
        'total': total,
        'page': page,
        'size': size,
        'books': [book.to_dict() for book in books]
    })
