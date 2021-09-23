from datetime import date

import pytest

from capitulo.authentication.services import AuthenticationException
from capitulo.books import services as books_services
from capitulo.authentication import services as auth_services
from capitulo.books.services import NonExistentBookException
from capitulo.reading_list import services as read_services
from capitulo.utilities import services as util_services


def test_can_add_user(in_memory_repo):
    new_user_name = 'jz'
    new_password = 'abcd1A23'

    auth_services.add_user(new_user_name, new_password, in_memory_repo)

    user_as_dict = auth_services.get_user(new_user_name, in_memory_repo)
    assert user_as_dict['user_name'] == new_user_name

    # Check that password has been encrypted.
    assert user_as_dict['password'].startswith('pbkdf2:sha256:')


def test_cannot_add_user_with_existing_name(in_memory_repo):
    with pytest.raises(auth_services.NameNotUniqueException):
        auth_services.add_user('thorke', 'abcd1A23', in_memory_repo)


def test_can_get_user(in_memory_repo):
    user = auth_services.get_user('thorke', in_memory_repo)
    assert user is not None


def test_authentication_with_valid_credentials(in_memory_repo):
    new_user_name = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_user_name, new_password, in_memory_repo)

    try:
        auth_services.authenticate_user(new_user_name, new_password, in_memory_repo)
    except AuthenticationException:
        assert False


def test_authentication_with_invalid_credentials(in_memory_repo):
    new_user_name = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_user_name, new_password, in_memory_repo)

    with pytest.raises(auth_services.AuthenticationException):
        auth_services.authenticate_user(new_user_name, '0987654321', in_memory_repo)


def test_can_add_reviews(in_memory_repo):
    user_name = 'pmccartney'
    password = 'abcd1A23'
    auth_services.add_user(user_name, password, in_memory_repo)
    book_id = 27036539
    review_text = 'scary!'

    # Call the service layer to add the comment.
    books_services.add_review(book_id, review_text, user_name, 4, in_memory_repo)

    # Retrieve the comments for the article from the repository.
    reviews_as_dict = books_services.get_reviews_for_book(book_id, in_memory_repo)

    # Check that the comments include a comment with the new comment text.
    assert next(
        (dictionary['review_text'] for dictionary in reviews_as_dict if dictionary['review_text'] == review_text),
        None) is not None


def test_cannot_add_review_for_non_existent_book(in_memory_repo):
    user_name = 'pmccartney'
    password = 'abcd1A23'
    auth_services.add_user(user_name, password, in_memory_repo)
    book_id = 123
    review_text = "what is this"

    # Call the service layer to attempt to add the comment.
    with pytest.raises(books_services.NonExistentBookException):
        books_services.add_review(book_id, review_text, user_name, 4, in_memory_repo)


def test_cannot_add_review_by_unknown_user(in_memory_repo):
    book_id = 27036539
    review_text = 'hungry'
    user_name = 'gmichael'

    # Call the service layer to attempt to add the comment.
    with pytest.raises(books_services.UnknownUserException):
        books_services.add_review(book_id, review_text, user_name, 4, in_memory_repo)


def test_can_get_book(in_memory_repo):
    book_id = 27036539

    book_as_dict = books_services.get_book(book_id, in_memory_repo)

    assert book_as_dict['id'] == book_id
    assert book_as_dict['title'] == 'War Stories, Volume 4'
    assert len(book_as_dict['reviews']) == 0
    assert book_as_dict['release_year'] == 2016
    assert book_as_dict['image_hyperlink'] == 'https://images.gr-assets.com/books/1453685087m/27036539.jpg'
    assert book_as_dict['ebook'] == False
    assert book_as_dict['num_pages'] == 144


def test_cannot_get_book_with_non_existent_id(in_memory_repo):
    book_id = 3423524

    # Call the service layer to attempt to retrieve the book.
    with pytest.raises(books_services.NonExistentBookException):
        books_services.get_book(book_id, in_memory_repo)


def test_get_books_by_id(in_memory_repo):
    target_book_ids = [27036539, 23272155, 56353, 8356365]
    books_as_dict = books_services.get_books_by_id(target_book_ids, in_memory_repo)

    # Check that 2 books were returned from the query.
    assert len(books_as_dict) == 2

    # Check that the book ids returned were 27036539 and 23272155.
    book_ids = [book['id'] for book in books_as_dict]
    assert set([27036539, 23272155]).issubset(book_ids)


def test_get_book_ids_for_language(in_memory_repo):
    book_ids = books_services.get_book_ids_for_language("Japanese", in_memory_repo)
    assert len(book_ids) == 1


def test_cannot_get_book_ids_for_non_existent_language(in_memory_repo):
    book_ids = books_services.get_book_ids_for_language("dog", in_memory_repo)
    assert book_ids is None


def test_get_books_by_author(in_memory_repo):
    book_ids = books_services.get_books_by_author("Garth Ennis", in_memory_repo)
    assert len(book_ids) == 2


def test_cannot_get_book_ids_for_non_existent_author(in_memory_repo):
    book_ids = books_services.get_book_ids_for_author("dog", in_memory_repo)
    assert book_ids == []


def test_get_book_ids_for_publisher(in_memory_repo):
    book_ids = books_services.get_books_by_publisher("DC Comics", in_memory_repo)
    assert len(book_ids) == 1


def test_cannot_get_book_ids_for_non_existent_publisher(in_memory_repo):
    book_ids = books_services.get_book_ids_for_author("dog", in_memory_repo)
    assert book_ids == []


def test_get_book_ids_for_release_year(in_memory_repo):
    book_ids = books_services.get_books_by_release_year(1997, in_memory_repo)
    assert len(book_ids) == 1


def test_cannot_get_book_ids_for_non_existent_year(in_memory_repo):
    book_ids = books_services.get_book_ids_for_year(100, in_memory_repo)
    assert book_ids == None


def test_can_get_books_by_author(in_memory_repo):
    books = books_services.get_books_by_author("Garth Ennis", in_memory_repo)
    assert len(books) == 2


def test_can_get_books_by_publisher(in_memory_repo):
    books = books_services.get_books_by_publisher("DC Comics", in_memory_repo)
    assert len(books) == 1


def test_can_get_books_by_release_year(in_memory_repo):
    books = books_services.get_books_by_release_year(1997, in_memory_repo)
    assert len(books) == 1


def test_can_get_languages(in_memory_repo):
    languages = util_services.get_languages(in_memory_repo)
    assert len(languages) == 6


def test_can_get_authors(in_memory_repo):
    authors = util_services.get_authors(in_memory_repo)
    assert len(authors) == 31


def test_can_get_publishers(in_memory_repo):
    publishers = util_services.get_publishers(in_memory_repo)
    assert len(publishers) == 12


def test_can_get_release_years(in_memory_repo):
    years = util_services.get_release_years(in_memory_repo)
    assert len(years) == 8
    assert 1997 in years
    assert 2011 in years


def test_can_get_all_books(in_memory_repo):
    books = util_services.get_all_books(in_memory_repo)
    assert len(books) == 20


def test_can_get_books_by_author(in_memory_repo):
    books = util_services.get_books_by_author("Mike Wolfer", in_memory_repo)
    assert books[0].title == "Crossed, Volume 15"


def test_get_reviews_for_book(in_memory_repo):
    user_name = 'gmichael'
    password = 'abcd1A23'
    auth_services.add_user(user_name, password, in_memory_repo)
    books_services.add_review(27036539, 'wow', 'gmichael', 2, in_memory_repo)
    books_services.add_review(27036539, 'just wow', 'gmichael', 1, in_memory_repo)
    reviews_as_dict = books_services.get_reviews_for_book(27036539, in_memory_repo)

    # Check that 2 reviews were returned for the book with id 27036539.
    assert len(reviews_as_dict) == 2

    # Check that the reviews relate to the book whose id is 27036539.
    book_ids = [review['book_id'] for review in reviews_as_dict]
    book_ids = set(book_ids)
    assert 27036539 in book_ids and len(book_ids) == 1


def test_get_reviews_for_non_existent_book(in_memory_repo):
    with pytest.raises(NonExistentBookException):
        reviews_as_dict = books_services.get_reviews_for_book(3448848, in_memory_repo)


def test_get_reviews_for_book_without_reviews(in_memory_repo):
    reviews_as_dict = books_services.get_reviews_for_book(27036539, in_memory_repo)
    assert len(reviews_as_dict) == 0


def test_get_reading_list_for_user(in_memory_repo):
    user_name = 'gmichael'
    password = 'abcd1A23'
    auth_services.add_user(user_name, password, in_memory_repo)
    reading_list = read_services.get_reading_list('gmichael', in_memory_repo)
    assert len(reading_list) == 0


def test_cannot_get_reading_list_without_user(in_memory_repo):
    with pytest.raises(read_services.UnknownUserException):
        reading_list = read_services.get_reading_list('gmichael', in_memory_repo)


def test_gives_correct_readings_list_for_users(in_memory_repo):
    user_name1 = 'dogdog'
    password1 = 'abcd1A23'
    auth_services.add_user(user_name1, password1, in_memory_repo)
    read_services.add_book_to_reading_list(27036539, user_name1, in_memory_repo)
    reading_list1 = read_services.get_reading_list('dogdog', in_memory_repo)

    user_name2 = 'gmichael'
    password2 = 'dfdkdkdk34'
    auth_services.add_user(user_name2, password2, in_memory_repo)
    read_services.add_book_to_reading_list(23272155, user_name2, in_memory_repo)
    reading_list2 = read_services.get_reading_list('gmichael', in_memory_repo)

    assert reading_list1 != reading_list2
    assert reading_list1[0] != reading_list2[0]


def test_add_book_to_reading_list_for_user(in_memory_repo):
    user_name = 'dogdog'
    password = 'catcat3434'
    auth_services.add_user(user_name, password, in_memory_repo)
    reading_list = read_services.get_reading_list('dogdog', in_memory_repo)
    read_services.add_book_to_reading_list(27036539, user_name, in_memory_repo)
    read_services.add_book_to_reading_list(23272155, user_name, in_memory_repo)
    assert len(reading_list) == 2


def test_cannot_add_book_to_reading_list_without_user(in_memory_repo):
    with pytest.raises(read_services.UnknownUserException):
        read_services.add_book_to_reading_list(27036539, None, in_memory_repo)
    # Non existent user
    with pytest.raises(read_services.UnknownUserException):
        read_services.add_book_to_reading_list(27036539, 'efesfs', in_memory_repo)


def test_cannot_add_book_to_reading_list_without_book(in_memory_repo):
    user_name = 'dogdog'
    password = 'catcat3434'
    auth_services.add_user(user_name, password, in_memory_repo)
    with pytest.raises(read_services.NonExistentBookException):
        read_services.add_book_to_reading_list(None, 'dogdog', in_memory_repo)
    with pytest.raises(read_services.NonExistentBookException):
        read_services.add_book_to_reading_list(3567543, 'dogdog', in_memory_repo)


def test_remove_book_from_reading_list_for_user(in_memory_repo):
    user_name = 'dogdog'
    password = 'catcat3434'
    auth_services.add_user(user_name, password, in_memory_repo)
    reading_list = read_services.get_reading_list(user_name, in_memory_repo)
    read_services.add_book_to_reading_list(27036539, user_name, in_memory_repo)
    read_services.add_book_to_reading_list(23272155, user_name, in_memory_repo)
    assert len(reading_list) == 2
    read_services.remove_book_from_reading_list(27036539, user_name, in_memory_repo)
    assert len(reading_list) == 1
    read_services.remove_book_from_reading_list(23272155, user_name, in_memory_repo)
    assert len(reading_list) == 0


def test_cannot_remove_book_from_reading_list_without_user(in_memory_repo):
    with pytest.raises(read_services.UnknownUserException):
        read_services.remove_book_from_reading_list(27036539, None, in_memory_repo)
    # Non existent user
    with pytest.raises(read_services.UnknownUserException):
        read_services.remove_book_from_reading_list(27036539, 'efesfs', in_memory_repo)


def test_cannot_remove_book_from_reading_list_without_book(in_memory_repo):
    user_name = 'dogdog'
    password = 'catcat3434'
    auth_services.add_user(user_name, password, in_memory_repo)
    with pytest.raises(read_services.NonExistentBookException):
        read_services.add_book_to_reading_list(None, 'dogdog', in_memory_repo)
    with pytest.raises(read_services.NonExistentBookException):
        read_services.add_book_to_reading_list(3567543, 'dogdog', in_memory_repo)
