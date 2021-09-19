"""Initialize Flask app."""

from pathlib import Path

from flask import Flask

import capitulo.adapters.repository as repo
from capitulo.adapters.memory_repository import MemoryRepository, populate



def create_app(test_config=None):

    # Create the flask app object
    app = Flask(__name__)

    # Configure the app from configuration-file settings.
    app.config.from_object('config.Config')
    data_path = Path('capitulo') / 'adapters' / 'data'

    if test_config is not None:
        # Load test configuration, and override any configuration settings.
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']
    
    # Create the MemoryRepository implementation for a memory-based repository.
    repo.repo_instance = MemoryRepository()
    # fill the content of the repository from the provided csv files
    populate(data_path, repo.repo_instance)

    #Build the application
    with app.app_context():
        #Register blueprints
        from .home import home
        app.register_blueprint(home.home_blueprint)

        from .about_us import about_us
        app.register_blueprint(about_us.about_us_blueprint)

        from .books import books
        app.register_blueprint(books.books_blueprint)

        from .authentication import authentication
        app.register_blueprint(authentication.authentication_blueprint)

        from .utilities import utilities
        app.register_blueprint(utilities.utilities_blueprint)

        from .reading_list import reading_list
        app.register_blueprint(reading_list.reading_list_blueprint)

    return app