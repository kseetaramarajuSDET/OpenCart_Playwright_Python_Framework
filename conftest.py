from pathlib import Path
import allure
import pytest
import logging

from playwright.sync_api import Playwright

from api.users_api import UsersAPI
from config import Config
from utilities.custom_logger import LogGen  # 🚀 Hooking up your centralized custom logging framework
import os
import platform


# ========================================================================
# STEP 1: ADD COMMAND LINE OPTIONS
# ========================================================================
def pytest_addoption(parser):
    """
        Adds custom command line options.
        Only declare options here that are NOT natively provided by pytest-playwright.
        """
    # Keep your custom key-value headless toggle flag we built earlier!
    parser.addoption("--headless", default="False", help="Force headless background run: True or False")
    # Keep your custom screenshot and tracing options (Playwright doesn't declare these as standard CLI flags)
    # parser.addoption("--screenshot", default="only-on-failure", help="Take screenshot: on, off, only-on-failure")
    # parser.addoption("--tracing", default="retain-on-failure", help="Tracing: on, off, retain-on-failure")
    # Helper to read configuration values cleanly


def get_config_value(config, option_name):
    """
    Helper to read configuration values cleanly.
    Safely sanitizes list arrays returned by native engine parameters.
    """
    cmd_value = config.getoption(option_name)

    if cmd_value is not None:
        # 🚀 ANTI-CRASH SAFEGUARD: If Pytest wraps the option inside a list, grab the first element!
        if isinstance(cmd_value, list):
            return cmd_value[0] if cmd_value else None
        return cmd_value

    return config.getini(option_name)


# ========================================================================
# STEP 2: HOOK TO TRACK TEST RESULTS (PASS/FAIL)
# ========================================================================
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Boot up the custom logger context configuration properties dynamically [cite: 1575]
    LogGen.loggen()
    log = logging.getLogger("Pytest_Engine_Spy")

    outcome = yield
    report = outcome.get_result()
    setattr(item, f"rep_{report.when}", report)

    # Log out severe verification crashes live inside the call execution phase [cite: 574]
    if report.when == "call" and report.failed:
        log.error(f"❌ TEST TRAGEDY RECORDED! Test target method '{item.name}' CRASHED during step execution.")


# ========================================================================
# STEP 3: FIXTURE 1 - BROWSER CONTEXT SETUP (Leveraging Native Playwright)
# ========================================================================
@pytest.fixture(scope="function")
def browser_context(request, playwright):  # <-- Injected native 'playwright' fixture
    LogGen.loggen()
    log = logging.getLogger("Browser_Context_Fixture")

    browser_name = get_config_value(request.config, "browser").lower()
    video_option = get_config_value(request.config, "video")
    # 1. Grab the string value ("True" or "False") from terminal or pytest.ini
    headless_raw = get_config_value(request.config, "headless")
    # 2. Convert that string value safely into a real Python Boolean
    headed_flag = str(headless_raw).lower() in ("true", "1", "yes", "t")

    # 🎯 VISUAL LOGGING LOGIC REPAIRED: Correctly prints true human readability parameters!
    log.info(
        f"Preparing engine lifecycle switches. Launching browser browser: '{browser_name}' | Headed: {headed_flag}")

    # Launch browser dynamically using the built-in instance
    launch_args = ["--start-maximized"] if browser_name in ("chromium", "chrome", "edge") else []

    if browser_name in ("chromium", "chrome"):
        browser = playwright.chromium.launch(headless=headed_flag, args=launch_args)
    elif browser_name == "firefox":
        browser = playwright.firefox.launch(headless=headed_flag)
    elif browser_name == "webkit":
        browser = playwright.webkit.launch(headless=headed_flag)
    else:
        log.critical(f"Aborting execution! Unsupported browser engine specified: '{browser_name}'")
        raise ValueError(f"❌ Unsupported browser: {browser_name}")

        # Setup context options context parameters
    context_args = {}
    if video_option in ["on", "retain-on-failure"]:
        log.info("Media recording parameter detected as ACTIVE. Directing video output files path to: 'reports/videos'")
        context_args["record_video_dir"] = "reports/videos"

    # Enforce true desktop maximization for Chromium engines
    if browser_name in ("chromium", "chrome"):
        context_args["no_viewport"] = True
    else:
        context_args["viewport"] = {"width": 1920, "height": 1080}

    log.info("Spanning secure isolated browser context profile container window.")
    context = browser.new_context(**context_args)
    yield context

    # Post-Test cleanup checks for low-level automation hooks
    log.info("Wiping environment memory allocations. Terminating active browser profile context channels.")
    # Final backup cleanup safeguard
    context.close()
    browser.close()


# ========================================================================
# STEP 4: FIXTURE 2 - PAGE AND ARTIFACT MANAGEMENT
# ========================================================================
@pytest.fixture(scope="function")
def page(request, browser_context):
    LogGen.loggen()
    log = logging.getLogger("Page_Artifact_Fixture")

    base_url = get_config_value(request.config, "base_url")
    screenshot_option = get_config_value(request.config, "screenshot")
    tracing_option = get_config_value(request.config, "tracing")
    video_option = get_config_value(request.config, "video")

    test_name = request.node.name

    if tracing_option in ["on", "retain-on-failure"]:
        log.info(f"[{test_name}] - Background tracing authorized. Deploying continuous diagnostic timeline monitors.")
        browser_context.tracing.start(screenshots=True, snapshots=True, sources=True)

    log.info(f"[{test_name}] - Opening clean workspace page tab canvas session.")
    page = browser_context.new_page()
    if base_url:
        log.info(f"[{test_name}] - Routing browser tab viewport gateway target URL to: '{base_url}'")
        page.goto(base_url)

    yield page

    # Capture state post-yield
    test_name = request.node.name
    test_failed = hasattr(request.node, "rep_call") and request.node.rep_call.failed
    log.info(
        f"[{test_name}] - Automation sequence complete. Reconciling test outcome metrics. Failed status: {test_failed}")
    # Cache the physical video path file pointer while the page tab session is alive
    video_path = page.video.path() if page.video else None

    # 1. Stop and Save Tracing
    if tracing_option in ["on", "retain-on-failure"]:
        trace_path = f"reports/traces/{test_name}_trace.zip"
        log.info(
            f"[{test_name}] - Closing timeline track loop handles. Compressing trace archives to zip: '{trace_path}'")
        browser_context.tracing.stop(path=trace_path)

        if test_failed:
            # FIX: Native Zip mapping configuration for Allure Report Viewer
            log.info(
                f"[{test_name}] - Attaching diagnostic zip trace logs payload directly to Allure Report viewer index.")
            allure.attach.file(
                trace_path,
                name=f"{test_name}_playwright_trace",
                attachment_type="application/zip"
            )
        else:
            log.info(
                f"[{test_name}] - Test passed cleanly. Unlinking passing trace zip off local disk data directories.")
            Path(trace_path).unlink(missing_ok=True)

    # 2. Capture and Save Failure Screenshots
    if test_failed and screenshot_option in ["on", "only-on-failure"]:
        screenshot_path = f"reports/screenshots/{test_name}.png"
        log.info(f"[{test_name}] - Capturing visual crash verification screenshot image file path: '{screenshot_path}'")
        page.screenshot(path=screenshot_path)
        allure.attach.file(
            screenshot_path,
            name=f"{test_name}_failure_screenshot",
            attachment_type=allure.attachment_type.PNG
        )

    # 🚀 THE CRITICAL TEARDOWN SEQUENCER FIX:
    # Explicitly close the targets here AFTER artifacts are captured and saved.
    # This securely unlocks all trailing media buffer write handlers for Windows!
    log.info(f"[{test_name}] - Detaching system tab sessions and driver handles. Severing file locks.")
    page.close()
    browser_context.close()

    # 3. Capture and Save Videos
    if video_option in ["on", "retain-on-failure"]:
        video_path = page.video.path() if page.video else None
        # Video is fully processed only after the context finishes closing
        if not test_failed and video_option == "retain-on-failure" and video_path:
            log.info(
                f"[{test_name}] - Execution passed cleanly. Purging non-failure media recordings from file paths storage: '{video_path}'")
            # Clean up unwanted videos from passing tests locally
            Path(video_path).unlink(missing_ok=True)
        elif test_failed and video_path and Path(video_path).exists():
            log.info(
                f"[{test_name}] - Verification step failed. Preserving recording and linking .webm video clip to Allure dashboard.")
            allure.attach.file(
                video_path,
                name=f"{test_name}_failure_video",
                attachment_type=allure.attachment_type.WEBM
            )


# ==========================================
# API AUTOMATION FIXTURES (HYBRID SETUP)
# ==========================================

@pytest.fixture(scope="session")
def api_request_context(playwright: Playwright):
    LogGen.loggen()
    log = logging.getLogger("api_request_context")
    """
    Creates a centralized API Context for the entire test run.
    Scope is 'session' so it only initializes once (super fast!).
    """
    log.info("\n[ conftest.py ] -> Initializing Playwright API Context...")

    request_context = playwright.request.new_context(
        base_url=Config.GOREST_BASE_URL,
        extra_http_headers=Config.GOREST_HEADERS
    )

    yield request_context

    log.info("\n[ conftest.py ] -> Disposing Playwright API Context...")
    request_context.dispose()


@pytest.fixture
def users_api(api_request_context):
    """
    Passes the API context into our UsersAPI Service Class.
    Any test that requests 'users_api' will get this ready-to-use object.
    """
    return UsersAPI(api_request_context)


# ==========================================
# ALLURE REPORTING - ENVIRONMENT WIDGET
# ==========================================

def pytest_sessionfinish(session, exitstatus):
    """
    This hook runs automatically after all tests have finished executing.
    It generates the environment.properties file for Allure.
    """
    LogGen.loggen()
    log = logging.getLogger("pytest_session_finish")
    log.info("\n[ conftest.py ] -> Generating Allure Environment details...")

    allure_dir = session.config.getoption("--alluredir")

    if allure_dir:
        os.makedirs(allure_dir, exist_ok=True)

        # 🌟 NEW LOGIC: Figure out what suite was run by checking the '-m' flag
        # 'markexpr' grabs whatever you typed after '-m' (e.g., 'api', 'ui')
        markexpr = session.config.getoption("markexpr", default="")

        if "api" in markexpr.lower():
            run_type = "API Automation Suite"
        elif "ui" in markexpr.lower():
            run_type = "UI Automation Suite"
        elif markexpr:
            run_type = f"Custom Run ({markexpr})"
        else:
            run_type = "Full Hybrid Suite (UI + API)"

        # 2. Gather the universal data
        env_data = {
            "Execution_Environment": "QA / Staging",
            "Test_Suite_Executed": run_type,
            "Operating_System": f"{platform.system()} {platform.release()}",
            "Python_Version": platform.python_version(),
            "Framework": "Playwright + Pytest Hybrid"
        }

        # 🌟 BULLETPROOF LOGIC: Directly check the raw terminal marker
        is_api_run = "api" in markexpr.lower()

        # 3. Try to grab UI-specific data (Browser flags)
        if not is_api_run:
            try:
                browser = session.config.getoption("--browser")
                headless = session.config.getoption("--headless")
                if browser:
                    env_data["Browser"] = browser[0].capitalize()
                if headless is not None:
                    env_data["Headless_Mode"] = str(headless)
            except ValueError:
                pass  # It was an API run, skip the UI stuff!

        # 4. Write the data into the exact file Allure expects
        env_file_path = os.path.join(allure_dir, "environment.properties")
        with open(env_file_path, "w") as f:
            for key, value in env_data.items():
                f.write(f"{key}={value}\n")
