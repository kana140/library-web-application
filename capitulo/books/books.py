import math

from flask import Blueprint
from flask import request, render_template, redirect, url_for, session

from better_profanity import profanity
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

import capitulo.adapters.repository as repo
import capitulo.utilities.utilities as utilities
import capitulo.books.services as services

from capitulo.authentication.authentication import login_required

# Configure the Blueprint
books_blueprint = Blueprint( 'books_bp', __name__)

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
    books = services.get_books_by_id(book_ids[(page - 1) * books_per_page : page * books_per_page], repo.repo_instance)

    number_of_pages = math.ceil(len(book_ids) / books_per_page)

    # Note that we will display the number of pages, and we need to remember to inform the request.args of our page number.
    page_list = []
    for i in range(1, number_of_pages + 1):
        page_list.append(url_for('books_bp.books_by_language', page=i, language=language_name))
    
    # Generate the template
    return render_template(
        'books/books.html',
        search_title = language_name,
        page_list = page_list,
        books = books,
        language_urls = utilities.get_languages_and_urls()
    )