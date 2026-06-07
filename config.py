# ========================================================================
# config.py - FRAMEWORK DATA & ENVIRONMENT CONFIGURATION MANAGEMENT
# ========================================================================
import os


class Config:
    """
    Centralized Configuration Repository.
    Reads values dynamically from the OS Environment variables (CI/CD / Terminal),
    and falls back to standard hardcoded defaults for local debugging in PyCharm.
    """

    # ------------------------------------------------------------------------
    # Application Target Environment & Test Credentials
    # ------------------------------------------------------------------------
    BASE_URL = os.getenv("base_url", "https://tutorialsninja.com/demo")
    USERNAME = os.getenv("test_username", "kseetaramaraju1@gmail.com")
    PASSWORD = os.getenv("test_password", "Seeta@123")

    # ------------------------------------------------------------------------
    # Core Framework Timeouts (Playwright uses milliseconds)
    # ------------------------------------------------------------------------
    # Default implicit timeout for actions like .click(), .fill(), .goto() (10 Seconds)
    DEFAULT_TIMEOUT = int(os.getenv("default_timeout", "10000"))

    # Timeout window for web-first assertions like expect(locator).to_be_visible() (5 Seconds)
    EXPECT_TIMEOUT = int(os.getenv("expect_timeout", "5000"))

    # ------------------------------------------------------------------------
    # Browser Type Settings
    # ------------------------------------------------------------------------
    # Default core test engine selection (chromium, chrome, edge, firefox, webkit)
    BROWSER_TYPE = os.getenv("browser_type", "chromium")

    # Converts terminal/system string variables safely into true Python Booleans
    HEADLESS = os.getenv("headless", "False").lower() in ("true", "1", "t", "yes")