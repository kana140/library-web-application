import pytest

from flask import session


def test_register(client):
    # Check that we retrieve the register page.
    response_code = client.get('/authentication/register').status_code
    assert response_code == 200

    # Check that we can register a user successfully, supplying a valid user name and password.
    response = client.post(
        '/authentication/register',
        data={'user_name': 'gmichael', 'password': 'CarelessWhisper1984'}
    )
    assert response.headers['Location'] == 'http://localhost/authentication/login'


@pytest.mark.parametrize(('user_name', 'password', 'message'), (
        ('', '', b'Your user name is required'),
        ('cj', '', b'Your user name is too short'),
        ('test', '', b'Your password is required'),
        ('test', 'test',
         b'Your password must be at least 8 characters, and contain an upper case letter, a lower case letter and a digit'),
        ('fmercury', 'Test#6^0', b'Your user name is already taken - please supply another'),
))
def test_register_with_invalid_input(client, user_name, password, message):
    # Check that attempting to register with invalid combinations of user name and password generate appropriate error
    # messages.
    response = client.post(
        '/authentication/register',
        data={'user_name': user_name, 'password': password}
    )
    assert message in response.data


def test_login(client, auth):
    # Check that we can retrieve the login page.
    status_code = client.get('/authentication/login').status_code
    assert status_code == 200

    # Check that a successful login generates a redirect to the homepage.
    response = auth.login()
    assert response.headers['Location'] == 'http://localhost/'

    # Check that a session has been created for the logged-in user.
    with client:
        client.get('/')
        assert session['user_name'] == 'thorke'


# Bad key error

def test_logout(client, auth):
    # Login a user.
    auth.login()

    with client:
        # Check that logging out clears the user's session.
        auth.logout()
        assert 'user_id' not in session


def test_index(client):
    # Check that we can retrieve the home page.
    response = client.get('/')
    assert response.status_code == 200
    assert b'Welcome to Capitulo!' in response.data


def test_login_required_to_review(client):
    response = client.post('/review')
    assert response.headers['Location'] == 'http://localhost/authentication/login'


def test_review(client, auth):
    # Login a user.
    auth.login()

    # Check that we can retrieve the reviews page.
    response = client.get('/23272155')
    assert b'terrible, just terrible' in response.data

    response = client.post(
        '/review?book=23272155',
        data={'review': 'who reads this?', 'rating': 4, 'book_id': 23272155}
    )
    assert response.headers['Location'] == 'http://localhost/23272155?view_reviews_for=23272155'


def test_review_page(client):
    # Check that we can retrieve the books page
    response = client.get('/707611?view_reviews_for=707611')
    assert response.status_code == 200

    # Check that all reviews are included on the page (will be 0 in this case)
    assert b'0 Reviews' in response.data

    response = client.get('/23272155?view_reviews_for=23272155')
    assert b'terrible, just terrible' in response.data


@pytest.mark.parametrize(('review', 'rating', 'messages'), (
        ('Who thinks the author is a fuckwit?', 5, (b'Your review must not contain profanity')),
        ('Hey', 4, (b'Your review is too short')),
        ('ass', 3, (b'Your review is too short', b'Your review must not contain profanity')),
))
def test_review_with_invalid_input(client, auth, review, rating, messages):
    # Login a user
    auth.login()

    # Attempt to review a book
    response = client.post(
        '/review?book=707611',
        data={'review': review, 'rating': rating, 'book_id': 707611}
    )
    # Check that supplying invalid review text generates appropriate error messages.
    for message in messages:
        assert message in response.data


def test_login_required_for_reading_list(client):
    response = client.post('/reading_list')
    assert response.headers['Location'] == 'http://localhost/authentication/login'


def test_cannot_add_book_to_reading_list_with_invalid_input(client, auth):
    auth.login()
    response = client.post('/reading_list/add_book/707')
    assert response.status_code != 200


def test_about_us_page(client):
    response = client.get('/About_Us')
    assert response.status_code == 200


def test_cannot_remove_book_from_reading_list_with_invalid_input(client, auth):
    auth.login()
    response = client.post('/reading_list/remove_book/5678')
    assert response.status_code != 200


def test_books_with_language(client):
    # Check that we can retrieve page depending on language chosen
    response = client.get('/books_by_language?language=English')
    assert response.status_code == 200

    # Check that the page includes the first book
    assert b'Books in English' in response.data


def test_books_with_author(client):
    # Check that we can retrieve page depending on author chosen
    response = client.get('/books_by_author?author_name=Andrea+DiVito')
    assert response.status_code == 200

    # Check that the page includes the first book
    assert b'Books by Andrea DiVito' in response.data


def test_books_with_publisher(client):
    # Check that we can retrieve page depending on publisher chosen
    response = client.get('/books_by_publisher?publisher_name=DC+Comics')
    assert response.status_code == 200

    # Check that the page includes the first book
    assert b'Books from DC Comics' in response.data


def test_books_with_release_year(client):
    # Check that we can retrieve page depending on language chosen
    response = client.get('/books_by_release_year?release_year=1997')
    assert response.status_code == 200

    # Check that the page includes the first book
    assert b'Books from 1997' in response.data
