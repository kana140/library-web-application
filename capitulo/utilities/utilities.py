from flask import Blueprint, request, render_template, redirect, url_for, session

import capitulo.adapters.repository as repo
import capitulo.utilities.services as services

# Configure the Blueprint
utilities_blueprint = Blueprint('utilities_bp', __name__)

def get_languages_and_urls():
    languages = services.get_languages(repo.repo_instance)
    language_urls = dict()
    for language in languages:
        language_urls[language] = url_for('books_bp.books_by_language', language=language)
    return language_urls


