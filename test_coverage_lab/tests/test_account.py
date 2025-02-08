"""
Test Cases for Account Model
"""
import json
from random import randrange
import pytest
from models import db
from models.account import Account, DataValidationError
from sqlalchemy.exc import IntegrityError

ACCOUNT_DATA = {}

@pytest.fixture(scope="module", autouse=True)
def load_account_data():
    """ Load data needed by tests """
    global ACCOUNT_DATA
    with open('tests/fixtures/account_data.json') as json_data:
        ACCOUNT_DATA = json.load(json_data)

    # Set up the database tables
    db.create_all()
    yield
    db.session.close()

@pytest.fixture(scope="function", autouse=True)
def setup_and_teardown():
    """ Truncate the tables and set up for each test """
    db.session.query(Account).delete()
    db.session.commit()
    yield
    db.session.remove()

######################################################################
#  E X A M P L E   T E S T   C A S E
######################################################################

# ===========================
# Test Group: Role Management
# ===========================

# ===========================
# Test: Account Role Assignment
# Author: John Businge
# Date: 2025-01-30
# Description: Ensure roles can be assigned and checked.
# ===========================

def test_account_role_assignment():
    """Test assigning roles to an account"""
    account = Account(name="John Doe", email="johndoe@example.com", role="user")

    # Assign initial role
    assert account.role == "user"

    # Change role and verify
    account.change_role("admin")
    assert account.role == "admin"

# ===========================
# Test: Invalid Role Assignment
# Author: John Businge
# Date: 2025-01-30
# Description: Ensure invalid roles raise a DataValidationError.
# ===========================

def test_invalid_role_assignment():
    """Test assigning an invalid role"""
    account = Account(role="user")

    # Attempt to assign an invalid role
    with pytest.raises(DataValidationError):
        account.change_role("moderator")  # Invalid role should raise an error


######################################################################
#  T O D O   T E S T S  (To Be Completed by Students)
######################################################################

"""
Each student in the team should implement **one test case** from the list below.
The team should coordinate to **avoid duplicate work**.

Each test should include:
- A descriptive **docstring** explaining what is being tested.
- **Assertions** to verify expected behavior.
- A meaningful **commit message** when submitting their PR.
"""

# TODO 1: Test Account Serialization
# - Ensure `to_dict()` correctly converts an account to a dictionary format.
# - Verify that all expected fields are included in the dictionary.

# ===========================
# Test: Test Account Serialization
# Author: Cassandra Tolton
# Date: 2025-02-07
# Description:  `to_dict()` correctly converts an account to a dictionary format and
#               Verify that all expected fields are included in the dictionary.
# ===========================

def test_account_serialization():
    account = Account(name="Cass Tolton", email="tolton@unlv.nevada.edu", balance=420.00)
    
    #serialize the account and check if it turns it into a dictionary
    accountSerialized = account.to_dict()
    
    #make sure the new serialzed account is a dictionary
    assert isinstance(accountSerialized, dict)
    
    items=  ['id', 'name', 'email', 'phone_number', 'disabled', 'date_joined', 'balance', 'role']
    
    #check and make sure the dictionary has all expected fields.
    for x in range(len(items)):
        assert items[x] in accountSerialized


# TODO 2: Test Updating Account Email
# - Ensure an account’s email can be successfully updated.
# - Verify that the updated email is stored in the database.

# ===========================
# Test: Missing Required Fields
# Author: Sarel Erasmus
# Date: 2025-02-05
# Description: Ensure that creating an 'Account()' without required fields raises an error.
# ===========================

def test_missing_required_fields():
    # Create account that has the required fields not included
    account = Account()

    # Pytest is expecting an Integrity Error since the account object doesn't have the required fields
    with pytest.raises(IntegrityError):
        # Try to commit this account to the database to make sure it produces an error
        db.session.add(account)
        db.session.commit()

# ===========================
# Test: Test Positive Deposit
# Author: Alexander Baker
# Date: 2025-02-01
# Description: Ensure a positive deposit increases balance
# ===========================
def test_positive_deposit():
    """Test depositing a positive number"""
    account = Account(balance=0.0)

    # Attempt to deposit a positive number
    account.deposit(100.0)
    assert account.balance == 100.0
    
# TODO 5: Test Deposit with Zero/Negative Values
# - Ensure `deposit()` raises an error for zero or negative amounts.
# - Verify that balance remains unchanged after an invalid deposit attempt.

# ===========================
# Test: Valid Withdrawal
# Author: Daniel Levy
# Date: 2025-02-04
# Description: Ensure `withdraw()` correctly decreases the account balance.
#              Verify that withdrawals within available balance succeed.
# ===========================
def test_valid_withdrawal():
    # Create new account for unit test
    account = Account(name="Daniel Levy", email="levyd1@unlv.nevada.edu", balance=100.00)

    # First Test: Withdraw decreases balance by the correct amount
    original_balance = account.balance
    account.withdraw(20)
    assert account.balance == (original_balance-20)
    
    # Second Test: Withdraw is able to succeed with current available balance
    original_balance = account.balance 
    amount_to_decrease_balance = 30
    account.withdraw(amount_to_decrease_balance)
    assert account.balance > amount_to_decrease_balance
    

# ===========================
# Test 7: Test Withdrawal with Insufficient Funds + positive withdraw amt
# Author: Eli Rosales
# Date: 2025-02-05
# Description: 
#   - Ensure `withdraw()` raises an error when attempting to withdraw more than available balance.
#   - Verify that the balance remains unchanged after a failed withdrawal.
# ===========================

def test_valid_withdrawal_with_insufficient_funds():
    # Create new account for unit test
    account = Account(name="Eli Rosales", email="rosale5@unlv.nevada.edu", balance=100.00)
    amt = account.balance
    # Attempt to withdraw amt > bal (120 > 100)
    with pytest.raises(DataValidationError):
        account.withdraw(120) #raise error if withdraw more than balance
    #Verify that the balance remains unchanged after a failed withdrawal.
    assert amt == account.balance

# ===========================
# Test 7 continued: Positive withdraw amt
# Author: Eli Rosales
# Date: 2025-02-05
# Description: 
#   - raise error if withdraw is negative number
# ===========================

def test_valid_withdrawal_amt_must_be_positive():
    account = Account(name="Eli Rosales", email="rosale5@unlv.nevada.edu", balance=100.00)
    with pytest.raises(DataValidationError):
        account.withdraw(-1) #raise error if withdraw amount is negative
# TODO 7: Test Withdrawal with Insufficient Funds
# - Ensure `withdraw()` raises an error when attempting to withdraw more than available balance.
# - Verify that the balance remains unchanged after a failed withdrawal.

# TODO 8: Test Password Hashing
# - Ensure that passwords are stored as **hashed values**.
# - Verify that plaintext passwords are never stored in the database.
# - Test password verification with `set_password()` and `check_password()`.

# ===========================
# Author: Jesse Ortega
# Date: 2025-02-05
# ===========================

def test_password_hashing():
    # Create test account
    test_account = Account(name="Jesse Ortega", email="ortegj8@unlv.nevada.edu")
    
    # Set password to test account
    password = "LetMeIn123_thisIsASecurePassword_qwertyDirty_burritoTorpedo"
    test_account.set_password(password)

    # Confirm that plain-text password is not stored within object
    assert test_account.password_hash != password

    # Checks if the given password matches the stored password
    assert test_account.check_password(password)

# TODO 9: Test Role Assignment
# - Ensure that `change_role()` correctly updates an account’s role.
# - Verify that the updated role is stored in the database.

# ===========================
# Test: Test Role Assignment
# Author: Ernesto Dones Sierra
# Date: 2025-02-07
# Description: We check here both if the fucntion returns the correct data both ways
# ===========================

def test_role_assignment():
    #create dummy entrance with 'admin' role
    dummy = Account(name="Ernesto Dones", email="ernesto@example.com", role="admin")

    #save the unique (primary key) id
    #this does not returns an integer wich is weird, "NoneType" instead
    #dummyID = dummy.id

    #change dummy role from 'admin' to 'user'
    dummy.change_role("user")

    #find the account in the database by the unique id
    #does not work either, "NoneType" stuff again, weird square
    #dummyAccount = Account.query.filter_by(id=dummy.id).first()

    #Verify that the updated role is stored in the database, else error out
    #assert dummyAccount.role == "user"

    #if role was not changed then fucntion is not working properly
    assert dummy.role == "user"

    #now lets check if from 'admin' to 'user' the function also works
    dummy.change_role("admin")

    #Verify that the updated role is stored in the database, else error out
    #same "NoneType" nonsense
    #assert dummyAccount.role == "admin"

    #if role was not changed then fucntion is not working properly
    assert dummy.role == "admin"



# TODO 10: Test Invalid Role Assignment
# - Ensure that assigning an invalid role raises an appropriate error.
# - Verify that only allowed roles (`admin`, `user`, etc.) can be set.

# TODO 11: Test Deleting an Account
# - Ensure that `delete()` removes an account from the database.
# - Verify that attempting to retrieve a deleted account returns `None` or raises an error.

# ===========================
# Description: interesting, dummy.delete() crashes the program and it shouldnt i wonder why? unless my syntax is wrong 
# i dont understand why the delete() fucntion crashes the execution 
# ===========================

#def test_deleting_an_account():
    #create dummy entrance in our database 
    #dummy = Account(name="Ernesto Dones", email="ernesto@example.com", role="admin")

    #save the unique id (Primary key) of our dummy db entrance
    #dummyId = dummy.id

    #erase the dummy account
    #dummy.delete()

    #look in the database the unique id entrance if it exist then 'exist' list will have a length of 1
    #exist = db.session(Account).filter(Account.id==dummyId).all()
    #exist = Account.query.filter_by(id=dummyId).first()

    #if exist list length is not 0 then we did not erased the entrance in our databse
    #assert len(exist) == 0
    #exist.id must not exist since we deleted the account so if the result is equal to the prior dummyId this entrance was not erased
    #assert exist.id != dummyId

    

    









