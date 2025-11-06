from playwright.sync_api import expect, sync_playwright

from app import demo


def test_calculator_basic_operations():
    """Test basic calculator operations through the UI."""
    _, url, _ = demo.launch(prevent_thread_lock=True)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.set_default_timeout(1000)
            page.goto(url)

            page.get_by_label("First Number").click()
            page.get_by_label("First Number").fill("3")
            page.get_by_label("Second Number (ignored for").click()
            page.get_by_label("Second Number (ignored for").fill("4")
            page.get_by_role("button", name="Calculate").click()
            locator = page.get_by_test_id("textbox")
            expect(locator).to_have_value("7")

            browser.close()
    finally:
        demo.close()


def test_calculator_square_operation():
    """Test that second input disappears for Square operation."""
    _, url, _ = demo.launch(prevent_thread_lock=True)

    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.set_default_timeout(1000)
            page.goto(url)

            locator = page.get_by_label("Second Number (ignored for Square)")
            expect(locator).to_be_visible()
            page.get_by_label("Operation").click()
            page.get_by_label("First Number").fill("3")
            page.locator("#component-4 div").filter(has_text="Operation").locator(
                "div"
            ).nth(2).click()
            page.get_by_label("Square", exact=True).click()
            locator = page.get_by_label("Second Number (ignored for Square)")
            expect(locator).to_be_hidden()

            browser.close()
    finally:
        demo.close()


def test_calculator_division_by_zero():
    """Test division by zero error handling."""
    # Launch the demo
    _, url, _ = demo.launch(prevent_thread_lock=True)
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.set_default_timeout(1000)
            page.goto(url)

            page.get_by_label("First Number").click()
            page.get_by_label("First Number").fill("4")
            page.get_by_label("Operation").click()
            page.get_by_label("Divide").click()
            page.get_by_role("button", name="Calculate").click()
            locator = page.get_by_test_id("toast-body").get_by_text("Error", exact=True)
            expect(locator).to_be_visible()

            browser.close()
    finally:
        demo.close()
