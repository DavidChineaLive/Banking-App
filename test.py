import unittest
import function

class TestDepositFunds(unittest.TestCase):
    def setUp(self):
        # Connect to the database and create a test account
        self.mydb = function.connect_to_database()
        self.account_number = function.generate_account_number()
        function.create_account(self.mydb, 'testuser', 'testpassword', 'test@example.com', '1234', account_number=self.account_number)

    def tearDown(self):
        # Delete the test account and close the database connection
        function.delete_account(self.mydb, self.account_number)
        function.close_connection(self.mydb)

    def test_deposit_funds(self):
        # Test depositing funds into the test account
        function.deposit_funds(self.mydb, self.account_number, 100)
        balance = function.check_balance(self.mydb, self.account_number)
        self.assertEqual(balance, 100)


class TestWithdrawFunds(unittest.TestCase):
    def setUp(self):
        # Connect to the database and create a test account
        self.mydb = function.connect_to_database()
        self.account_number = function.generate_account_number()
        function.create_account(self.mydb, 'testuser', 'testpassword', 'test@example.com', '1234', account_number=self.account_number)
        # Deposit some funds into the test account
        function.deposit_funds(self.mydb, self.account_number, 100)

    def tearDown(self):
        # Delete the test account and close the database connection
        function.delete_account(self.mydb, self.account_number)
        function.close_connection(self.mydb)

    def test_withdraw_funds(self):
        # Test withdrawing funds from the test account
        function.withdraw_funds(self.mydb, self.account_number, 50, 100)
        balance = function.check_balance(self.mydb, self.account_number)
        self.assertEqual(balance, 50)


class TestCreateAccount(unittest.TestCase):
    def test_create_account(self):
        # Test creating a new account
        mydb = function.connect_to_database()
        function.create_account(mydb, 'testuser', 'testpassword', 'test@example.com', '1234')
        account_number = function.generate_account_number(mydb, 'testuser')
        self.assertIsNotNone(account_number)
        function.delete_account(mydb, account_number)
        function.close_connection(mydb)



if __name__ == '__main__':
    unittest.main()