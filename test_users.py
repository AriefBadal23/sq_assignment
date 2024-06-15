import os
import unittest
from sqlite3 import connect
from managers import user_manager, profile_manager
from entities.user import User
from entities.profile import Profile
from config import Config
from utils import (
    load_private_key,
    load_public_key,
    generate_registration_date,
    rsa_encrypt,
    rsa_decrypt,
)


class TestUsers(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """This method runs once before all tests."""
        ...

    @classmethod
    def tearDownClass(cls):
        """This method runs once after all tests."""
        ...

    def setUp(self):
        """This method runs before each test."""
        TestUsers.config = Config(
            connect("test.db"), load_public_key(), load_private_key()
        )
        TestUsers.user_manager = user_manager.UserManager(TestUsers.config)
        TestUsers.profile_manager = profile_manager.ProfileManager(TestUsers.config)

        TestUsers.user_manager.initialize()
        TestUsers.profile_manager.initialize()

        SQL_CREATE_USER = """
            INSERT INTO users (username, password, role) VALUES (?, ?, ?);
        """
        encrypted_username = rsa_encrypt("consultant_0", TestUsers.config.public_key)
        encrypted_password = rsa_encrypt("Admin_123?", TestUsers.config.public_key)
        encrypted_role = rsa_encrypt(
            User.Role.CONSULTANT.value, TestUsers.config.public_key
        )

        SQL_CREATE_PROFILE = """
            INSERT INTO profiles (first_name, last_name, registration_date, user_id)
            VALUES (?, ?, ?, ?);
        """
        encrypted_first_name = rsa_encrypt("John", TestUsers.config.public_key)
        encrypted_last_name = rsa_encrypt("Doe", TestUsers.config.public_key)
        encrypted_registration_date = rsa_encrypt(
            generate_registration_date(), TestUsers.config.public_key
        )

        try:
            cursor = TestUsers.config.con.cursor()
            cursor.execute(
                SQL_CREATE_USER,
                (encrypted_username, encrypted_password, encrypted_role),
            )
            TestUsers.config.con.commit()

            cursor.execute(
                SQL_CREATE_PROFILE,
                (
                    encrypted_first_name,
                    encrypted_last_name,
                    encrypted_registration_date,
                    1,
                ),
            )
            TestUsers.config.con.commit()
        finally:
            cursor.close()

    def tearDown(self):
        """This method runs after each test."""
        os.remove("test.db")

    def test_create_user_and_profile(self):
        """Test creating a new user and profile record."""
        # arrange user
        user = User(
            id=None,
            username="SysAdmin0",
            password="Admin_123?",
            role=User.Role.SYSTEM_ADMIN.value,
        )

        # act user
        created_user = TestUsers.user_manager.create_user(
            user.username, user.password, user.role
        )

        # arrange profile
        profile = Profile(
            id=None,
            first_name="John",
            last_name="Doe",
            registration_date=None,
            user_id=created_user.id,
        )

        # act profile
        created_profile = TestUsers.profile_manager.create_profile(
            profile.first_name, profile.last_name, profile.user_id
        )

        # assert user
        self.assertIsNotNone(created_user.id)
        self.assertEqual(created_user.username, user.username)

        # assert profile
        self.assertEqual(created_profile.user_id, created_user.id)
        self.assertIsNotNone(created_profile.id)
        self.assertIsNotNone(created_profile.registration_date)
        self.assertEqual(created_profile.first_name, profile.first_name)

    def test_get_list_users_profiles(self):
        """Test reading a list of user and profile records."""
        # act
        users = TestUsers.user_manager.get_users()
        profiles = TestUsers.profile_manager.get_profiles()

        # assert
        self.assertEqual(users[0].id, profiles[0].user_id)

    def test_get_user_profile(self):
        """Test reading a single user and profile record."""
        # act
        user = TestUsers.user_manager.get_user(1)
        profile = TestUsers.profile_manager.get_profile(1)

        # assert
        self.assertEqual(user.id, profile.user_id)

    def test_update_users_profile(self):
        """Test updating a user and profile record."""
        # arrange
        user = TestUsers.user_manager.get_user(1)
        profile = TestUsers.profile_manager.get_profile(1)

        # act
        user.username = "SysAdmin1"
        TestUsers.user_manager.update_user(
            user, user.username, user.password, user.role
        )

        profile.first_name = "Jane"
        TestUsers.profile_manager.update_profile(
            profile, profile.first_name, profile.last_name
        )

        # assert
        updated_user = TestUsers.user_manager.get_user(1)
        updated_profile = TestUsers.profile_manager.get_profile(1)

        self.assertEqual(updated_user.username, user.username)
        self.assertEqual(updated_profile.first_name, profile.first_name)

    def test_delete(self):
        """Test deleting a user record and the consequent deletion of a profile."""
        # arrange
        user = TestUsers.user_manager.get_user("consultant_0")

        # act
        TestUsers.user_manager.delete_user(user)

        # assert
        deleted_user = TestUsers.user_manager.get_user("consultant_0")
        deleted_profile = TestUsers.profile_manager.get_profile(user.id)

        self.assertIsNone(deleted_user)
        self.assertIsNone(deleted_profile)


if __name__ == "__main__":
    unittest.main()
