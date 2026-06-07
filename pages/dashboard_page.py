# ========================================================================
# pages/dashboard_page.py - THE ROUTING PORTAL AND APPLICATION HUB
# ========================================================================
from pages.base_page import BasePage  # 🚀 Corrected Parent Engine Inheritance Link
from pages.login_page import LoginPage  # 🚀 Imported for complete Page Chaining flow


class DashboardPage(BasePage):  # ✅ Inherits cleanly from BasePage
    # ------------------------------------------------------------------------
    # 1. Strictly Isolated Element Locators (Private Naming Conventions)
    # ------------------------------------------------------------------------
    _desktopsLink = "//a[normalize-space()='Desktops']"
    _myAccountLink = "//a[@title='My Account']"

    # 🎯 CRITICAL ELEMENT ISOLATION LAYER BOUNDARY FIX:
    # Scopes the Login path selection explicitly inside the active top-bar dropdown 
    # list to avoid crashing into duplicate static column link text wrappers!
    _loginLink = "//ul[@class='dropdown-menu dropdown-menu-right']//a[normalize-space()='Login']"
    _registerLink = "//ul[@class='dropdown-menu dropdown-menu-right']//a[normalize-space()='Register']"
    _myOrdersHeader = "//h2[normalize-space()='My Orders']"

    # ------------------------------------------------------------------------
    # 2. Page Actions Behavior Flows and Verification Checks
    # ------------------------------------------------------------------------
    def is_myOrders_header_visible(self) -> bool:
        """Validates if the user session landed successfully inside the target Dashboard view."""
        self.log.info(f"Initiating visual state assertion check for element layout header: '{self._myOrdersHeader}'")
        is_visible_status = self.page.is_visible(self._myOrdersHeader)

        if is_visible_status:
            self.log.info("Dashboard validation milestone confirmed. My Orders heading text is VISIBLE.")
        else:
            self.log.warning("Dashboard validation milestone unfulfilled. My Orders heading text is HIDDEN.")

        return is_visible_status

    def navigate_to_login_page(self) -> LoginPage:
        """
        Safely opens the top application navigation menu layout container, 
        selects the isolated Login option link, and chains control to the LoginPage.
        """
        self.log.info("Executing top bar interaction pathway loop to unfold profile dashboard link choices.")

        # Step A: Click 'My Account' layout text element to open up the dropdown choices 🔓
        self.click_element(self._myAccountLink)

        # Step B: Click the isolated Login option link sitting cleanly inside that open drop panel container
        self.click_element(self._loginLink)

        # 🚀 PAGE CHAINING ENGINE: 
        # Instantly instantiate and return the next correct view context page layout
        self.log.info("Navigation transition verified. Returning initialized LoginPage Object context.")
        return LoginPage(self.page)
