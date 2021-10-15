from flask import request, Blueprint, render_template, url_for

import math

import capitulo.adapters.repository as repo
import capitulo.utilities.utilities as utilities
import capitulo.home.services as services

from wtforms import Form, StringField, SelectField

home_blueprint = Blueprint('home_bp', __name__)


@home_blueprint.route('/', methods=['GET', 'POST'])
def home():
    books_per_page = 4
    page = request.args.get('page')
    if page is None:
        page = 1
    else:
        page = int(page)
    q = request.args.get('q')
    books = services.get_all_books(repo.repo_instance)
    results = []
    if q:
        for book in books:
            if q.lower() in (book.get('title')).lower():
                results.append(book)
            for author in book.get('authors'):
                if q.lower() in (author.get('full_name')).lower():
                    results.append(book)
            if book.get('publisher') != None and q.lower() in (book.get('publisher').name).lower():
                results.append(book)
            if q.lower() in str(book.get('release_year')).lower():
                results.append(book)
        for language in utilities.get_languages():
            if q.lower() in language.lower():
                for language_book in services.get_books_by_language(language, repo.repo_instance):
                    results.append(language_book)
    
    books_to_return = results[(page - 1) * books_per_page : page * books_per_page]
    number_of_pages = math.ceil(len(results) / books_per_page)
    page_list = []
    for i in range(1, number_of_pages + 1):
        page_list.append(url_for('home_bp.home', page=i, q=q))
    

    return render_template('home/home.html',
        books=books_to_return,
        page_list=page_list,
        q=q,
        language_urls=utilities.get_languages_and_urls(),
        author_urls=utilities.get_authors_and_urls(),
        publisher_urls=utilities.get_publishers_and_urls(),
        release_year_urls=utilities.get_release_years_and_urls()
    )