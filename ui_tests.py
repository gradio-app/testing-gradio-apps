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
            page.locator("#component-4 div").filter(has_text="Operation").locator("div").nth(2).click()
            page.get_by_label("Square", exact=True).click()
            locator = page.get_by_label("Second Number (ignored for Square)")
            expect(locator).to_be_hidden()

            browser.close()
    finally:
        demo.close()


# def test_calculator_division_by_zero():
#     """Test division by zero error handling."""
#     # Launch the demo
#     _, url, _ = demo.launch(prevent_thread_lock=True)

#     try:
#         with sync_playwright() as p:
#             browser = p.chromium.launch()
#             page = browser.new_page()
#             page.goto(url)

#             # Wait for page to load
#             page.wait_for_selector("button:has-text('Calculate')")

#             # Select Divide operation
#             page.click(".dropdown")
#             page.click("text=Divide")

#             # Test division by zero
#             page.locator("input[aria-label='First Number']").fill("10")
#             page.locator("input[aria-label='Second Number (ignored for Square)']").fill(
#                 "0"
#             )
#             page.click("button:has-text('Calculate')")

#             # Wait for result and verify error message
#             page.wait_for_timeout(1000)
#             result_text = page.locator("textarea[aria-label='Result']").input_value()
#             assert "Error: Division by zero" in result_text

#             browser.close()
#     finally:
#         demo.close()
