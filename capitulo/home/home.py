from flask import request, Blueprint, render_template, url_for

import math

import capitulo.adapters.repository as repo
import capitulo.utilities.utilities as utilities
import capitulo.home.services as services

home_blueprint = Blueprint('home_bp', __name__)


@home_blueprint.route('/', methods=['GET'])
def home():
    books_per_page = 4

    page = request.args.get('page')

    if page is None:
        page = 1
    else:
        page = int(page)

    book_ids = services.get_book_ids_all(repo.repo_instance)

    books = services.get_books_by_id(book_ids[(page - 1) * books_per_page: page * books_per_page], repo.repo_instance)

    number_of_pages = math.ceil(len(book_ids) / books_per_page)

    page_list = []
    for i in range(1, number_of_pages + 1):
        page_list.append(url_for('home_bp.home', page=i))


    return render_template(
        'home/home.html',
        page_list=page_list,
        books=books,
        language_urls=utilities.get_languages_and_urls(),
        author_urls=utilities.get_authors_and_urls(),
        publisher_urls=utilities.get_publishers_and_urls(),
        release_year_urls=utilities.get_release_years_and_urls()
    )
