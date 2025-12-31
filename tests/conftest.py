import pytest

from app import data_store
from app import reviews


@pytest.fixture(autouse=True)
def reset_globals():
    """
    Ensures each test runs with a clean in-memory state.
    """
    # data_store
    data_store.USERS.clear()
    data_store.SCHOOLS.clear()
    data_store.clear_current_user()

    # reviews
    reviews.RATINGS.clear()
    reviews.COMMENTS.clear()
    reviews.FAVOURITES.clear()

    yield

    # cleanup again (safe)
    data_store.USERS.clear()
    data_store.SCHOOLS.clear()
    data_store.clear_current_user()
    reviews.RATINGS.clear()
    reviews.COMMENTS.clear()
    reviews.FAVOURITES.clear()
