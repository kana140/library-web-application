from flask import Blueprint, render_template

import capitulo.utilities.utilities as utilities

about_us_blueprint = Blueprint('about_us_bp', __name__)


@about_us_blueprint.route('/About_Us', methods=['GET'])
def about_us():
    return render_template(
        'about_us/about_us.html',
        language_urls=utilities.get_languages_and_urls(),
        author_urls=utilities.get_authors_and_urls(),
        publisher_urls=utilities.get_publishers_and_urls(),
        release_year_urls=utilities.get_release_years_and_urls()
    )
