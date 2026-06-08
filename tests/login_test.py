# ========================================================================
# tests/test_login.py - FUNCTIONAL AUTHENTICATION SUITE VALIDATION
# ========================================================================
import logging
import pytest
from tests.base_test import BaseTest
from config import Config
from utilities.yaml_reader import YamlReader


class TestLogin(BaseTest):
    # 🚀 Injected our dedicated test suite logging category scope
    log = logging.getLogger("TestSuite_Login")

    @pytest.mark.sanity
    def test_login_with_valid_credentials(self, request):
        self.log.info(f"🏁 EXECUTING TEST CASE: {request.node.name}")

        self.log.info(" Navigate to login page ")
        login_page_context = self.dashboard_page.navigate_to_login_page()

        self.log.info(f"**** Login Credentails : User={Config.USERNAME}, Expected={Config.PASSWORD} ****")
        login_page_context.execute_login(Config.USERNAME, Config.PASSWORD)

        self.log.info(" Sampling landing dashboard canvas elements to verify authorization state.")
        dashboard_landing_status = self.dashboard_page.is_myOrders_header_visible()

        # Perform structural engine verification
        assert dashboard_landing_status, "❌ Post-authentication validation failed! Dashboard layout header unrendered."

        self.log.info("🎉 TEST CASE CONCLUDED: SUCCESSFUL VALID AUTHENTICATION VERIFIED")

    test_data = YamlReader.read_logindata_from_yaml_file("test_data/loginData.yml")

    @pytest.mark.sanity
    @pytest.mark.parametrize("user, pwd, result", test_data)
    def test_login_with_valid_and_invalid_credentials(self, user, pwd, result, request):
        self.log.info(f"**** Starting Data Driven Test: User={user}, Expected={result} ****")

        self.log.info(f"🏁 EXECUTING TEST CASE: {request.node.name}")

        self.log.info(" Navigate to login page ")
        login_page_context = self.dashboard_page.navigate_to_login_page()

        self.log.info(f"**** Login Credentails : User={user}, Expected={pwd} ****")
        login_page_context.execute_login(user, pwd)

        if result == "pass":
            status = self.dashboard_page.is_myOrders_header_visible()
            if status:
                self.log.info(f"✅ Pass: Login worked as expected for user: {user}")
                assert True
            else:
                self.log.error(f"❌ Fail: Expected SUCCESS but login failed for: {user}")
                assert False
        elif result == "fail":
            status = self.login_page.get_login_error_message_text()
            if status:
                self.log.info(f"✅ Pass: Correctly showed error for invalid user: {user}")
                assert True
            else:
                self.log.error(f"❌ Fail: Expected error message for {user} was NOT displayed")
                assert False

        self.log.info("**** Finished Data Driven Test Case ****")
