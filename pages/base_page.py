# ========================================================================
# pages/base_page.py - THE PARENT ENGINE FOR ALL PAGE OBJECTS
# ========================================================================
import logging
from playwright.sync_api import Page

from config import Config
from utilities.custom_logger import LogGen  # 🚀 Clean link to your specific logger utility


class BasePage:
    def __init__(self, page: Page):
        """
        Accepts the live Playwright page instance from the fixture
        and shares it across all inherited Page Objects.
        """
        self.page = page

        # 1. Initialize your custom logger configurations permanently
        LogGen.loggen()

        # 2. 🎯 Dynamic Logger: Captures the native logging pipeline engine
        # and explicitly brands it with the exact child class name currently executing.
        self.log = logging.getLogger(self.__class__.__name__)

    def navigate_to(self, url: str):
        """Custom wrapper for page navigation with automated trace recording."""
        self.log.info(f"Initiating native browser window navigation to URL target: '{url}'")
        self.page.goto(url)

    def click_element(self, selector: str):
        """
        Optimized Wrapper: Explicitly waits for visibility, confirms the
        element is enabled/clickable, and executes the click action.
        """
        self.log.info(f"Targeting element. Scanning DOM tree canvas for visibility: '{selector}'")
        # 1. Wait for element to be physically drawn on the DOM web canvas
        element = self.page.wait_for_selector(selector, state="visible")

        # 2. Defensive Actionability Guard: Confirm it isn't greyed out or disabled
        if not element.is_enabled():
            self.log.error(f"Execution blocked! Target element locator is visible but locked/DISABLED: '{selector}'")
            raise RuntimeError(
                f"❌ Element Layer Element with locator '{selector}' is visible but DISABLED. Cannot click!")

        # 3. Perform the native click step safely
        self.log.info(f"Interactivity state verified as ENABLED. Firing click event on selector: '{selector}'")
        self.page.click(selector)

    def enter_text(self, selector: str, text: str):
        """
        Optimized Wrapper: Waits for visibility, verifies the input field is
        enabled, completely clears any pre-existing text data, and inputs new text.
        """
        self.log.info(f"Targeting element input field. Verifying visibility state: '{selector}'")
        # 1. Wait for input field to render visibly
        element = self.page.wait_for_selector(selector, state="visible")

        # 2. Defensive Actionability Guard: Ensure the text field isn't read-only or disabled
        if not element.is_enabled():
            self.log.error(f"Execution blocked! Target input field is visible but locked/DISABLED: '{selector}'")
            raise RuntimeError(f"❌ Input field with locator '{selector}' is visible but DISABLED. Cannot enter text!")

        # 3. Optimization Step: Highlight the element and wipe old placeholder/cached string text cleanly
        self.log.info(f"Purging stale characters, browser cache, and placeholders from selector: '{selector}'")
        self.page.locator(selector).clear()

        # 🔒 Security Guard Step: Avoid leaking real passwords in clean console texts/logs
        # If the selector has words like 'password' or 'pwd', replace it with asterisks in the console stream
        log_value = "********" if "password" in selector.lower() or "pwd" in selector.lower() else text

        # 4. Fill the input field cleanly
        self.log.info(f"Input stream authorized. Injecting value: '{log_value}' into selector: '{selector}'")
        self.page.fill(selector, text)

    def get_page_title(self) -> str:
        """Returns the current web browser tab text title."""
        title_text = self.page.title()
        self.log.info(f"Successfully scraped active browser tab page title string: '{title_text}'")
        return title_text

    # 🚀 Pro Move: Default the timeout parameter straight to your global Config variable!
    def is_element_displayed(self, selector: str, timeout_ms: int) -> bool:
        self.log.info(f"Checking visibility state. Maximum search window: {timeout_ms}ms")
        try:
            self.page.wait_for_selector(selector, state="visible", timeout=timeout_ms)
            return True
        except Exception:
            return False
