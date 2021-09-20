from flask import Blueprint
from flask import request, render_template, redirect, url_for, session

import capitulo.adapters.repository as repo
import capitulo.reading_list.services as services
import capitulo.utilities.utilities as utilities

# Configure the Blueprint
reading_list_blueprint = Blueprint('reading_list_bp', __name__)


@reading_list_blueprint.route('/reading_list', methods=['GET'])
def reading_list():
    read_list = services.get_reading_list(repo.repo_instance)
    # Construct urls for viewing reading list
    # for book in read_list:
    #     book['add_to_reading_list_url'] = url_for('reading_list_bp.add_book_to_reading_list()', book=book)

    return render_template('/reading_list.html', read_list=read_list,
        language_urls=utilities.get_languages_and_urls(),
        author_urls=utilities.get_authors_and_urls(),
        publisher_urls=utilities.get_publishers_and_urls(),
        release_year_urls=utilities.get_release_years_and_urls())  # Template for reading list


@reading_list_blueprint.route('/reading_list/book_added', methods=['GET', 'POST'])
def add_book_to_reading_list():
    book_id = int(request.args.get('book_id'))
    book = utilities.get_book(book_id)

    # Use the service layer to store the book into the reading list
    services.add_book_to_reading_list(book_id, repo.repo_instance)

    # New read list to pass into url
    read_list = services.get_reading_list(repo.repo_instance)

    # Cause the web browser to display the page of the reading list with the new added book, including old ones
    return redirect(url_for('reading_list_bp.reading_list', book=book, read_list=read_list))


@reading_list_blueprint.route('/reading_list/book_removed', methods=['GET', 'POST'])
def remove_book_from_reading_list():
    book_id = int(request.args.get('book_id'))
    book = utilities.get_book(book_id)

    # Use the service layer to remove the book from the reading list
    services.remove_book_from_reading_list(book_id, repo.repo_instance)

    # New read list to pass into url
    read_list = services.get_reading_list(repo.repo_instance)

    # Cause the web browser to display the page of the reading list with the new added book, including old ones
    return redirect(url_for('reading_list_bp.reading_list', book=book, read_list=read_list))
