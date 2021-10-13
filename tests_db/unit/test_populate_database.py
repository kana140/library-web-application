from sqlalchemy import select, inspect

from capitulo.adapters.orm import metadata

# def test_database_populate_inspect_table_names(database_engine):
    
#     # Get table information
#     inspector = inspect(database_engine)
#     assert inspector.get_table_names() == ['authors', 'books', 'book_authors', 'book_publishers', 'publishers', 'reading_list', 'reviews', 'users']

# def test_database_populate_select_all_users(database_engine):
    
#     # Get table information
#     inspector = inspect(database_engine)
#     name_of_users_table = inspector.get_table_names()[7]

#     with database_engine.connect() as connection:
#         # query for records in table tags
#         select_statement = select([metadata.tables[name_of_users_table]])
#         result = connection.execute(select_statement)

#         all_users = []
#         for row in result:
#             all_users.append(row['user_name'])

#         assert all_users == ['thorke', 'fmercury']