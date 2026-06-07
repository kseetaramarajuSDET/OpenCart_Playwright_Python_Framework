# ========================================================================
# tests/test_login.py - FUNCTIONAL AUTHENTICATION SUITE VALIDATION
# ========================================================================
import logging
import pytest
from tests.base_test import BaseTest
from config import Config


class TestLogin(BaseTest):
    # 🚀 Injected our dedicated test suite logging category scope
    log = logging.getLogger("TestSuite_Login")

    @pytest.mark.sanity
    def test_login_with_valid_credentials(self):
        """Validates standard authentication sequence flow using unified framework logging."""

        self.log.info("========================================================================")
        self.log.info("🏁 EXECUTING TEST CASE: Verify Authentication with Valid Credentials")
        self.log.info("========================================================================")

        # ------------------------------------------------------------------------
        # Step 1: UI Navigation Gateway Action Flow
        # ------------------------------------------------------------------------
        self.log.info("Step 1: Driving portal interaction path to reveal login elements panel.")
        # Utilizing our crisp Page Chaining pattern to capture the target page view context
        login_page_context = self.dashboard_page.navigate_to_login_page()

        # ------------------------------------------------------------------------
        # Step 2: Form Interaction and Token Dispatch Sequence
        # ------------------------------------------------------------------------
        self.log.info("Step 2: Transferring client system credentials into form collection fields.")
        login_page_context.execute_login(Config.USERNAME, Config.PASSWORD)

        # ------------------------------------------------------------------------
        # Step 3: Enterprise Validation and Milestone Assertion Logic
        # ------------------------------------------------------------------------
        self.log.info("Step 3: Sampling landing dashboard canvas elements to verify authorization state.")
        dashboard_landing_status = self.dashboard_page.is_myOrders_header_visible()

        # Perform structural engine verification
        assert dashboard_landing_status, "❌ Post-authentication validation failed! Dashboard layout header unrendered."

        self.log.info("========================================================================")
        self.log.info("🎉 TEST CASE CONCLUDED: SUCCESSFUL VALID AUTHENTICATION VERIFIED")
        self.log.info("========================================================================")