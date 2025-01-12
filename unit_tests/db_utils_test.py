import unittest
from unittest.mock import patch
from app import db_utils


class DbUtilsTest(unittest.TestCase):

    # Runs before every test to patch the connection to the DB
    def setUp(self):
        self.patcher = patch('database.db_utils.DbConnection')
        self.mock_db = self.patcher.start()
        self.addCleanup(self.patcher.stop)
        # A mock object is created when DbConnection is called
        self.mock_instance = self.mock_db.return_value
        self.mock_instance.fetch_data.return_value = [(1,)]
        self.mock_instance.commit_data.return_value = None
        self.mock_instance.close_connection.return_value = "DB connection closed."

    # TEST DBCONNECTION CLASS
    def test_DbConnection(self):
        # test class is instantiated
        db_instance = db_utils.DbConnection()
        self.mock_db.assert_called_once()
        self.assertEqual(db_instance.close_connection(), "DB connection closed.")
        self.mock_instance.close_connection.assert_called_once()


    # TEST INSERTING FUNCTIONS
    def test_add_new_user(self):
        # test correct input
        testing_user = {
            'FirstName': 'JJ',
            'LastName': 'Doe',
            'Username': 'jj',
            'email': 'jj@example.com',
            'hashed_password': 'hashedpassword123'
        }
        response = db_utils.add_new_user(testing_user)
        self.mock_instance.commit_data.assert_called_once()
        self.assertEqual(response, "New user added.")
        # test wrong input raises Exception
        self.assertRaises(TypeError, db_utils.add_new_user({}))
        self.assertRaises(TypeError, db_utils.add_new_user(['name', 'lastname', 'username', 'email', 'hashed_password']))
        self.assertRaises(TypeError, db_utils.add_new_user({'FirstName': 0, 'LastName': 0, 'Username': 0, 'email': 0, 'hashed_password': 0}))

    def test_add_journal(self):
        response = db_utils.add_journal('Today was a good day.', 1, '2023-05-15')
        self.mock_instance.commit_data.assert_called_once()
        self.assertEqual(response, "Diary entry added")
        self.assertRaises(Exception, db_utils.add_journal('asdaf', 100000, 20250201))

    def test_today_emotion(self):
        db_utils.today_emotion(1, 'happy', 'http://giphy.com/happy', '2023-05-15', 'J', 'Response')
        self.mock_instance.commit_data.assert_called_once()
        self.assertRaises(Exception, db_utils.today_emotion(2, 1, 1, 1, 1, 1))


    # TEST RETRIEVING FUNCTIONS
    def test_get_records(self):
        self.mock_instance.fetch_data.return_value = [(1, 'http://giphy.com', 'J', 'Response', 'Diary entry')]
        response = db_utils.get_records(1, '2023-05-15')
        self.mock_instance.fetch_data.assert_called_once()
        self.assertEqual(response, (1, 'http://giphy.com', 'J', 'Response', 'Diary entry'))
        self.assertRaises(Exception, db_utils.get_records('asdfa', '201201201'))

    def test_get_user_id(self):
        self.mock_instance.fetch_data.return_value = [(1,)]
        user_id = db_utils.get_user_id('johndoe')
        self.mock_instance.fetch_data.assert_called_once()
        self.assertEqual(user_id, 1)
        # test wrong input type
        self.mock_instance.fetch_data.return_value = []
        self.assertIsNone(db_utils.get_user_id(26))

    def test_get_month_emotions(self):
        self.mock_instance.fetch_data.return_value = [('happy', 5), ('sad', 2)]
        response = db_utils.get_month_emotions(1, 5, 2023)
        self.mock_instance.fetch_data.assert_called_once()
        self.assertEqual(response, [0, 0, 0, 5, 2, 0])
        # test wrong input
        self.mock_instance.fetch_data.return_value = []
        self.assertEqual([0, 0, 0, 0, 0, 0], db_utils.get_month_emotions('notint', 28, 'notyear'))

    def test_get_password(self):
        self.mock_instance.fetch_data.return_value = [('hashedpassword123',)]
        password = db_utils.get_password('johndoe')
        self.mock_instance.fetch_data.assert_called_once()
        self.assertEqual(password, 'hashedpassword123')
        # test wrong input
        self.mock_instance.fetch_data.return_value = []
        self.assertIsNone(db_utils.get_password(1))
        self.assertRaises(Exception, db_utils.get_password('notarealusername'))


    # TEST VALIDATING FUNCTIONS
    def test_check_entry_journal(self):
        self.mock_instance.fetch_data.return_value = [(1,)]
        self.assertTrue(db_utils.check_entry_journal(1, '2023-05-15'))
        self.mock_instance.fetch_data.assert_called_once()
        # test wrong input
        self.mock_instance.fetch_data.return_value = []
        self.assertFalse(db_utils.check_entry_journal(1239123124141, 16541201))
        self.assertRaises(Exception, db_utils.check_entry_journal(1239123124141, 'notadate'))

    def test_check_username(self):
        self.mock_instance.fetch_data.return_value = [(1,)]
        result = db_utils.check_username_exists('johndoe')
        self.mock_instance.fetch_data.assert_called_once()
        self.assertTrue(result)
        # test user not found
        self.mock_instance.fetch_data.return_value = []
        self.assertFalse(db_utils.check_username_exists(1))

    def test_check_email(self):
        self.mock_instance.fetch_data.return_value = [(1,)]
        result = db_utils.check_email_exists('john@example.com')
        self.mock_instance.fetch_data.assert_called_once()
        self.assertTrue(result)
        # test for email not found
        self.mock_instance.fetch_data.return_value = []
        self.assertFalse(db_utils.check_email_exists('notevenanemail'))
        self.assertRaises(Exception, db_utils.check_email_exists([]))
        self.assertEqual(0, db_utils.check_email_exists('notinthere'))

    def test_order_month_data(self):
        self.assertEqual([0, 0, 0, 0, 0, 0], db_utils.order_month_data([]))
        self.assertEqual([0, 0, 0, 0, 0, 0], db_utils.order_month_data([('test', 'test')]))
        self.assertEqual([3, 0, 0, 0, 0, 0], db_utils.order_month_data([('angry', 3)]))




if __name__ == "__main__":
    unittest.main()