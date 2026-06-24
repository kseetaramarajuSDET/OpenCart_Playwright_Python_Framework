import pytest
import time
from utilities.custom_logger import LogGen  # <--- Make sure your logger is imported!


@pytest.mark.api
class TestGoRestUsers:
    # Initialize the logger for the test class
    log = LogGen.loggen()
    # 1. We create Class Variables to share data between the independent tests
    user_id = None
    dynamic_name = f"SeetaRam_{int(time.time())}"
    dynamic_email = f"SeetaRam_{int(time.time())}@test.com"

    # ==========================================
    # INDIVIDUAL TESTS (Automating one by one)
    # ==========================================

    def test_create_user(self, users_api):
        self.log.info("********** STARTING TEST: Create New User **********")
        payload = {
            "name": self.dynamic_name,
            "gender": "male",
            "email": self.dynamic_email,
            "status": "active"
        }
        self.log.info(f"Test Step: Sending POST request to create user with email: {self.dynamic_email}")
        response = users_api.create_user(payload)
        self.log.info("Test Step: Validating response status code is 201")
        assert response.status == 201, "Failed to create user!"

        # Save the ID to the class so the next tests can use it!
        TestGoRestUsers.user_id = response.json()['id']
        self.log.info(f"Success: User created! Saved ID '{TestGoRestUsers.user_id}' for future tests.")
        self.log.info("********** TEST PASSED: Create New User **********\n")

    def test_get_user(self, users_api):
        self.log.info("********** STARTING TEST: Get Single User **********")

        self.log.info("Test Step: Verifying User ID exists from previous test")
        # We grab the ID that was saved by test_create_user
        assert TestGoRestUsers.user_id is not None, "User ID is missing! test_create_user might have failed."

        self.log.info(f"Test Step: Fetching user details for ID: {TestGoRestUsers.user_id}")
        response = users_api.get_user(TestGoRestUsers.user_id)
        self.log.info("Test Step: Validating response status code is 200")
        assert response.status == 200

        self.log.info(f"Test Step: Validating returned name matches '{self.dynamic_name}'")
        # Notice we assert against the dynamic variable here, not hardcoded text!
        assert response.json()['name'] == self.dynamic_name

        self.log.info("Success: Data validation successful!")
        self.log.info("********** TEST PASSED: Get Single User **********\n")

    def test_get_all_users(self, users_api):
        self.log.info("********** STARTING TEST: Get All Users **********")

        self.log.info("Test Step: Firing request to fetch the list of all users")
        # 1. Fire the request
        response = users_api.get_all_users()

        self.log.info("Test Step: Validating response status code is 200")
        # 2. Validate Status Code
        assert response.status == 200, f"Expected 200 OK, but got {response.status}"

        # Parse the JSON response
        users_list = response.json()
        self.log.info("Test Step: Validating response data type is a Python List")
        # 3. Validate Data Type (Ensure it actually returned a Python List)
        assert isinstance(users_list, list), "API did not return a list of users!"

        self.log.info("Test Step: Validating the list is not empty")
        # 4. Validate Size (Ensure the list is not empty)
        assert len(users_list) > 0, "The user database is completely empty!"

        # 5. Schema Validation (Pick the first user and verify it has the correct keys)
        first_user = users_list[0]

        self.log.info("Validating schema of the first user")
        # We verify the keys exist, but we don't hardcode values since data changes dynamically
        assert "id" in first_user, "User ID is missing from response!"
        assert "name" in first_user, "User name is missing!"
        assert "email" in first_user, "User email is missing!"
        assert "gender" in first_user, "User gender is missing!"
        assert "status" in first_user, "User status is missing!"

        self.log.info(f"Successfully fetched {len(users_list)} users. First user ID: {first_user['id']}")
        self.log.info("********** TEST PASSED: Get All Users **********\n")

    # def test_03_update_user(self, users_api):
    #     update_payload = {"name": "SeetaRam Updated"}
    #     response = users_api.update_user_partial(TestGoRestUsers.user_id, update_payload)
    #
    #     assert response.status == 200
    #     assert response.json()['name'] == "SeetaRam Updated"
    #
    # def test_04_delete_user(self, users_api):
    #     response = users_api.delete_user(TestGoRestUsers.user_id)
    #     assert response.status == 204
    #
    #     # Verify it's actually gone
    #     verify_response = users_api.get_user(TestGoRestUsers.user_id)
    #     assert verify_response.status == 404
    #
    # # ==========================================
    # # COMPLETE E2E FLOW (All in one shot)
    # # ==========================================
    #
    # def test_05_end_to_end_user_lifecycle(self, users_api):
    #     """This runs the entire flow in a single test script."""
    #
    #     # Generate fresh data just for this E2E test
    #     e2e_email = f"E2E_User_{int(time.time())}@test.com"
    #     e2e_name = f"E2E_User_{int(time.time())}"
    #
    #     # 1. POST
    #     create_response = users_api.create_user({
    #         "name": e2e_name, "gender": "male", "email": e2e_email, "status": "active"
    #     })
    #     assert create_response.status == 201
    #     e2e_id = create_response.json()['id']
    #
    #     # 2. GET
    #     get_response = users_api.get_user(e2e_id)
    #     assert get_response.status == 200
    #     assert get_response.json()['name'] == e2e_name
    #
    #     # 3. PATCH
    #     update_response = users_api.update_user_partial(e2e_id, {"name": "E2E Master"})
    #     assert update_response.status == 200
    #     assert update_response.json()['name'] == "E2E Master"
    #
    #     # 4. DELETE & VERIFY
    #     users_api.delete_user(e2e_id)
    #     verify_delete = users_api.get_user(e2e_id)
    #     assert verify_delete.status == 404
