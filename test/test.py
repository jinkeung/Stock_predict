import main.database_class as db

def test_set_user_data():
    join_success = db.set_user_data("TEST_ID", "TEST_PW", "TEST_NAME")
    print(join_success)
    assert join_success


