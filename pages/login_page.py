# ========================================================================
# pages/login_page.py - LOGIN PAGE FIELD OBJECT REPRESENTATION
# ========================================================================
from pages.base_page import BasePage  # ✅ Smooth inheritance from our parent engine


class LoginPage(BasePage):
    # ------------------------------------------------------------------------
    # 1. Page Element Locators (Isolate UI targets completely)
    # ------------------------------------------------------------------------
    _inputEmail = "#input-email"
    _inputPassword = "#input-password"
    _btnLogin = "//input[@value='Login']"
    _headerMyAccount = "//h2[normalize-space()='My Account']"
    _loginErrorMsg = "//div[@class='alert alert-danger alert-dismissible']"
    _logoutLink = "//a[@class='list-group-item'][normalize-space()='Logout']"

    # ------------------------------------------------------------------------
    # 2. Page Action Behaviors (Reusable action chains)
    # ------------------------------------------------------------------------
    def execute_login(self, username_value: str, password_value: str):
        """
        Performs end-to-end authentication sequence.
        Returns a fresh instance of the landing page to preserve page chaining.
        """
        self.log.info("Starting authentication transaction sequence block.")

        # Step A: Inject data securely into the Email text entry field ✉️
        self.enter_text(self._inputEmail, username_value)

        # Step B: Inject data securely into the Password field (Auto-masked by BasePage) 🔒
        self.enter_text(self._inputPassword, password_value)

        # Step C: Fire off the click event action on the submission element 🚀
        self.click_element(self._btnLogin)

        self.log.info("Authentication transaction dispatched. Page view transition in progress.")

        # NOTE: Once you create your next page object class (e.g., MyAccountPage),
        # you will add: 'return MyAccountPage(self.page)' right here to finish the chain!

    def get_error_message_text(self) -> str:
        """Scrapes and returns the dynamic text context from the login warning banner."""
        self.log.info("Initiating scan for runtime validation error alerts.")

        # Use our explicit visibility guard built right into BasePage structure
        self.page.wait_for_selector(self._loginErrorMsg, state="visible")
        error_text = self.page.locator(self._loginErrorMsg).inner_text()

        self.log.warning(f"Extracted active alert banner warning text: '{error_text.strip()}'")
        return error_text