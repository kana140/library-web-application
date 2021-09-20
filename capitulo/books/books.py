import math

from flask import Blueprint
from flask import request, render_template, redirect, url_for, session

from better_profanity import profanity
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField, IntegerField, validators
from wtforms.validators import DataRequired, Length, ValidationError

import capitulo.adapters.repository as repo
import capitulo.utilities.utilities as utilities
import capitulo.books.services as services

from capitulo.authentication.authentication import login_required

# Configure the Blueprint
books_blueprint = Blueprint('books_bp', __name__)


@books_blueprint.route('/<int:book_id>')
def individual_book(book_id):
    # Read query parameters.
    show_reviews = request.args.get('view_reviews_for')
    book = services.get_book(book_id, repo.repo_instance)
    book['add_review_url'] = url_for('books_bp.review_book', book=book['id'])
    return render_template('individual_book.html', book=book, show_reviews_for_book=show_reviews,
        author_urls=utilities.get_authors_and_urls(),
        language_urls=utilities.get_languages_and_urls(),
        publisher_urls=utilities.get_publishers_and_urls(),
        release_year_urls=utilities.get_release_years_and_urls()
    )


@books_blueprint.route('/books_by_language', methods=['GET'])
def books_by_language():
    books_per_page = 4

    # Read in the query parameters
    language_name = request.args.get('language')
    page = request.args.get('page')

    if page is None:
        page = 1
    else:
        page = int(page)

    # Retrieve book ids that have that are in the specified language
    book_ids = services.get_book_ids_for_language(language_name, repo.repo_instance)

    # Retrieve the set books we want to display based on the page
    books = services.get_books_by_id(book_ids[(page - 1) * books_per_page: page * books_per_page], repo.repo_instance)

    number_of_pages = math.ceil(len(book_ids) / books_per_page)

    # Note that we will display the number of pages, and we need to remember to inform the request.args of our page number.
    page_list = []
    for i in range(1, number_of_pages + 1):
        page_list.append(url_for('books_bp.books_by_language', page=i, language=language_name))

    # Generate the template
    return render_template(
        'books/books.html',
        search_title=language_name,
        page_list=page_list,
        books=books,
        language_urls=utilities.get_languages_and_urls(),
        word="in",
        author_urls=utilities.get_authors_and_urls(),
        publisher_urls=utilities.get_publishers_and_urls(),
        release_year_urls=utilities.get_release_years_and_urls()
    )


@books_blueprint.route('/books_by_author', methods=['GET'])
def books_by_author():
    books_per_page = 4

    # Read in the query parameters
    author_name = request.args.get('author_name')
    page = request.args.get('page')

    if page is None:
        page = 1
    else:
        page = int(page)

    books = services.get_books_by_author(author_name, repo.repo_instance)

    # Retrieve the set books we want to display based on the page
    # books = services.get_books_by_id(book_ids[(page - 1) * books_per_page: page * books_per_page], repo.repo_instance)

    number_of_pages = math.ceil(len(books) / books_per_page)

    # Note that we will display the number of pages, and we need to remember to inform the request.args of our page number.
    page_list = []
    for i in range(1, number_of_pages + 1):
        page_list.append(url_for('books_bp.books_by_author', page=i, author_name=author_name))

    # Generate the template
    return render_template(
        'books/books.html',
        search_title=author_name,
        page_list=page_list,
        books=books,
        author_urls=utilities.get_authors_and_urls(),
        word="by",
        language_urls=utilities.get_languages_and_urls(),
        publisher_urls=utilities.get_publishers_and_urls(),
        release_year_urls=utilities.get_release_years_and_urls()
    )


@books_blueprint.route('/books_by_publisher', methods=['GET'])
def books_by_publisher():
    books_per_page = 4

    # Read in the query parameters
    publisher_name = request.args.get('publisher_name')
    page = request.args.get('page')

    if page is None:
        page = 1
    else:
        page = int(page)

    books = services.get_books_by_publisher(publisher_name.strip(), repo.repo_instance)

    # Retrieve the set books we want to display based on the page
    # books = services.get_books_by_id(book_ids[(page - 1) * books_per_page: page * books_per_page], repo.repo_instance)

    number_of_pages = math.ceil(len(books) / books_per_page)

    # Note that we will display the number of pages, and we need to remember to inform the request.args of our page number.
    page_list = []
    for i in range(1, number_of_pages + 1):
        page_list.append(url_for('books_bp.books_by_publisher', page=i, publisher_name=publisher_name))

    # Generate the template
    return render_template(
        'books/books.html',
        search_title=publisher_name,
        page_list=page_list,
        books=books,
        publisher_urls=utilities.get_publishers_and_urls(),
        word="from",
        language_urls=utilities.get_languages_and_urls(),
        author_urls=utilities.get_authors_and_urls(),
        release_year_urls=utilities.get_release_years_and_urls()
    )


@books_blueprint.route('/books_by_release_year', methods=['GET'])
def books_by_release_year():
    books_per_page = 4

    # Read in the query parameters
    release_year = request.args.get('release_year')
    page = request.args.get('page')

    if page is None:
        page = 1
    else:
        page = int(page)

    books = services.get_books_by_release_year(int(release_year), repo.repo_instance)

    # Retrieve the set books we want to display based on the page
    # books = services.get_books_by_id(book_ids[(page - 1) * books_per_page: page * books_per_page], repo.repo_instance)

    number_of_pages = math.ceil(len(books) / books_per_page)

    # Note that we will display the number of pages, and we need to remember to inform the request.args of our page number.
    page_list = []
    for i in range(1, number_of_pages + 1):
        page_list.append(url_for('books_bp.books_by_release_year', page=i, release_year=release_year))

    # Generate the template
    return render_template(
        'books/books.html',
        search_title=release_year,
        page_list=page_list,
        books=books,
        release_year_urls=utilities.get_release_years_and_urls(),
        word="from",
        language_urls=utilities.get_languages_and_urls(),
        author_urls=utilities.get_authors_and_urls(),
        publisher_urls=utilities.get_publishers_and_urls()
    )


@books_blueprint.route('/review', methods=['GET', 'POST'])
@login_required
def review_book():
    # Obtain the user name of the currently logged in user.
    user_name = session['user_name']

    # Create form. The form maintains state, e.g. when this method is called with a HTTP GET request and populates
    # the form with a book id, when subsequently called with a HTTP POST request, the book id remains in the form
    form = ReviewForm()

    if form.validate_on_submit():
        # Successful POST, i.e. the review text has passed data validation.
        # Extract the book id, representing the reviewed book, from the form.
        book_id = int(form.book_id.data)

        # Use the service layer to store the new review.
        services.add_review(book_id, form.review.data, user_name, int(form.rating.data), repo.repo_instance)

        # Retrieve the book in dict form.
        book = services.get_book(book_id, repo.repo_instance)

        # Cause the web browser to display the page of the book with the new added review, including old ones
        return redirect(url_for('books_bp.individual_book', book_id=book_id, view_reviews_for=book_id))

    if request.method == 'GET':
        # Request is a HTTP GET to display the form.
        # Extract the book id, representing the book to review, from a query parameter of the GET request.
        book_id = int(request.args.get('book'))

        # Store the book id in the form
        form.book_id.data = book_id
    else:
        # Request is a HTTP POST where form validation has failed
        # Extract the book id of the book being reviewed from the form
        book_id = int(form.book_id.data)

    # For a GET or an unsuccessful POST, retrieve the book to review in dict form, and return a Web page that allows
    # the user to enter a comment. The generated Web page includes a form object.
    book = services.get_book(book_id, repo.repo_instance)
    return render_template(
        'books/book_review.html',
        title='Review Book',
        book=book,
        form=form,
        handle_url=url_for('books_bp.review_book'),
        language_urls=utilities.get_languages_and_urls(),
        author_urls=utilities.get_authors_and_urls(),
        publisher_urls=utilities.get_publishers_and_urls(),
        release_year_urls=utilities.get_release_years_and_urls()
    )


class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = u'Field must not contain profanity'
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)


class ReviewForm(FlaskForm):
    review = TextAreaField('Review', [
        DataRequired(),
        Length(min=4, message='Your review is too short'),
        ProfanityFree(message='Your comment must not contain profanity')])
    rating = IntegerField('Rating',
            validators=[validators.Required(), validators.NumberRange(min=1, max=5)])
    book_id = HiddenField("Book id")
    submit = SubmitField('Submit')
