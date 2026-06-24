# ========================================================================
# tests/base_test.py - THE STRUCTURAL FOUNDATION FOR ALL TEST SUITES
# ========================================================================
import logging
import pytest

from pages.dashboard_page import DashboardPage
from pages.login_page import LoginPage


@pytest.mark.usefixtures("page")
class BaseTest:
    """
    Parent class for all tests.
    Uses the 'page' fixture globally. Automatically builds out page object
    instances right before your test steps trigger.
    """

    # Python Type Hinting definitions to keep PyCharm autocomplete working perfectly
    login_page: LoginPage
    dashboard_page: DashboardPage

    # 🚀 Injected our structural test-layer logger utility context
    log = logging.getLogger("TestEngine_Setup")

    @pytest.fixture(autouse=True)
    def initialize_pages(self, page):
        """
        Wakes up automatically for every test case.
        Passes the active browser tab driver straight down into the constructor classes.
        """
        self.log.info("------------------------------------------------------------------------")
        self.log.info("🚀 Triggering background page lifecycle setup automation mapping pipeline.")
        self.log.info("------------------------------------------------------------------------")

        # 🎯 Instantiating and anchoring page context drivers straight to self
        self.log.info("Piping live browser driver handles straight into LoginPage constructor context.")
        self.login_page = LoginPage(page)

        self.log.info("Piping live browser driver handles straight into DashboardPage constructor context.")
        self.dashboard_page = DashboardPage(page)

        self.log.info("✅ Core UI Page Objects mapped cleanly to test context state. Ready for script steps.")