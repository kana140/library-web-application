from flask import Blueprint, render_template

import capitulo.utilities.utilities as utilities

home_blueprint = Blueprint('home_bp', __name__)

@home_blueprint.route('/', methods=['GET'])
def home():
    return render_template(
        'home/home.html',
        language_urls = utilities.get_languages_and_urls()
    )