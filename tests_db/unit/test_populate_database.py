from sqlalchemy import select, inspect

from capitulo.adapters.orm import metadata

import datetime

def test_database_populate_inspect_table_names(database_engine):
    
    # Get table information
    inspector = inspect(database_engine)
    assert inspector.get_table_names() == ['authors', 'book_authors', 'books', 'publishers', 'reading_lists', 'reviews', 'users']

def test_database_populate_select_all_users(database_engine):
    
    #Get table information
    inspector = inspect(database_engine)
    name_of_users_table = inspector.get_table_names()[6]

    with database_engine.connect() as connection:
        # Query for records in table users
        select_statement = select([metadata.tables[name_of_users_table]])
        result = connection.execute(select_statement)

        all_users = []
        for row in result:
            all_users.append(row['user_name'])
        
        assert all_users == ['thorke', 'fmercury', 'tyler']
    
def test_database_populate_select_all_reviews(database_engine):
    
    #Get table information
    inspector = inspect(database_engine)
    name_of_reviews_table = inspector.get_table_names()[5]

    with database_engine.connect() as connection:
        select_statement = select([metadata.tables[name_of_reviews_table]])
        results = connection.execute(select_statement)

        all_reviews = []
        for row in results:
            all_reviews.append((row['id'], row['user_id'], row['book_id'], row['review_text'], row['rating'], row['timestamp']))

        assert all_reviews == [(1,1,23272155,"Terrible, just terrible.",5, datetime.datetime(2020, 2, 28, 14, 31, 26)),
        (2,1,707611,"Best book ever, the best",5,datetime.datetime(2020, 2, 28, 14, 31, 26)),
        (3,1,707611,"Wow! This book was incredible. Super awe-inspiring",5, datetime.datetime(2020, 2, 28, 14, 31, 26)),
        (4,1,707611,"one of the best books ever, brings me back to the time i was a child and no one would talk to me not even my mum or dad good times",5,datetime.datetime(2020, 2, 28, 14, 31, 26)),
        (5,2,23272155,"AN ABSOLUTE ROMP",5,datetime.datetime(2020, 2, 28, 14, 32, 27)),
        (6,3,23272155,"This was the greatest thing Ive read since that time I fell over on the pavement and read what someone had written in the concrete when it when it was drying, you know how people do that? They wrote - nice dry -, like - nice try -, but it was in drying concrete! Isnt that just hilarious?!?! But yes this is the second best.",5,datetime.datetime(2020, 2, 28, 14, 32, 29))]

def test_database_populate_select_all_books(database_engine):

    #Get table information
    inspector = inspect(database_engine)
    name_of_books_table = inspector.get_table_names()[2]

    with database_engine.connect() as connection:
        #Query for records in table books
        select_statement = select([metadata.tables[name_of_books_table]])
        result = connection.execute(select_statement)

        all_books = []
        for row in result:
            all_books.append((row['id'], row['title'], row['book_id'], row['description'], row['publisher'], row['release_year'], row['num_pages'], row['image_hyperlink'], row['language']))
        
        number_of_books = len(all_books)
        
        assert number_of_books == 20
        assert all_books[0] == (1, 'The Switchblade Mamma', 25742454, "Lillian Ann Cross is forced to live the worst nightmare of her life. She is an everyday middle class American, striving to survive in an everyday changing world. Her life was abruptly\nturned upsidedown forever as she was kidnapped and forced into a world called \"Hen Fighting.\"\nA world in which women fight and bets are made upon their bloodshed.Lillian is forced to comply due to the threats made upon her mother's life. Being a loving person her whole life, Lillian finds difficulty grasping her new functions. As she is conditioned to live in her new world, she is subjected to an experimental procedure. A procedure which has taken the lives of a few before her. As she survives, she now has to learn how to live with her new \"implants.\" Implants which strengthen her bones, giving her strength and an upper ability amongst others. Implants which require weekly sustenance, or she will die.", None, None, None,'https://s.gr-assets.com/assets/nophoto/book/111x148-bcc042a9c91a29c1d680899eff700a03.png', 'English')
        
def test_database_populate_select_all_authors(database_engine):

    #Get table information
    inspector = inspect(database_engine)
    name_of_authors_table = inspector.get_table_names()[0]

    with database_engine.connect() as connection:
        #Query for records in table authors
        select_statement = select([metadata.tables[name_of_authors_table]])
        result = connection.execute(select_statement)

        all_authors = []
        for row in result:
            all_authors.append((row['id'], row['unique_id'], row['full_name']))
            print(row)
        
        assert all_authors[0] == (1, 8551671, "Lindsey Schussman")