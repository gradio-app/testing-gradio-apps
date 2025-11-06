# Example Gradio Calculator App & UI/UX Tests

This file contains a complete example of a Gradio calculator app and its associated Playwright UI/UX tests. You can use this as a reference when writing tests for your own Gradio applications.

## The Gradio App (`app.py`)

```python
import gradio as gr


def add(a, b):
    """Add two numbers."""
    return a + b


def subtract(a, b):
    """Subtract second number from first."""
    return a - b


def multiply(a, b):
    """Multiply two numbers."""
    return a * b


def divide(a, b):
    """Divide first number by second."""
    if b == 0:
        raise gr.Error("Error: Division by zero")
    return a / b


def square(a, b=None):
    """Square a number. Second parameter ignored."""
    return a * a


def calculate(operation, num1, num2):
    """Main calculation function that routes to appropriate operation."""
    if operation == "Add":
        return add(num1, num2)
    elif operation == "Subtract":
        return subtract(num1, num2)
    elif operation == "Multiply":
        return multiply(num1, num2)
    elif operation == "Divide":
        return divide(num1, num2)
    elif operation == "Square":
        return square(num1)
    else:
        return "Error: Unknown operation"


with gr.Blocks(title="Calculator App") as demo:
    gr.Markdown("# Simple Calculator")
    gr.Markdown("Choose an operation and enter numbers to calculate.")

    num1 = gr.Number(label="First Number", value=0)
    operation = gr.Dropdown(
        choices=["Add", "Subtract", "Multiply", "Divide", "Square"],
        label="Operation",
        value="Add",
    )
    num2 = gr.Number(label="Second Number (ignored for Square)", value=0)

    calculate_btn = gr.Button("Calculate", variant="primary")

    result = gr.Textbox(label="Result", interactive=False)

    def update_visibility(operation):
        if operation == "Square":
            return gr.Number(visible=False)
        else:
            return gr.Number(visible=True)

    operation.change(fn=update_visibility, inputs=operation, outputs=num2)

    calculate_btn.click(fn=calculate, inputs=[operation, num1, num2], outputs=result)

    gr.Markdown("### Examples")
    gr.Examples(
        examples=[
            ["Add", 5, 3],
            ["Subtract", 10, 4],
            ["Multiply", 6, 7],
            ["Divide", 15, 3],
            ["Square", 4, 0],
        ],
        inputs=[operation, num1, num2],
    )

if __name__ == "__main__":
    demo.launch()
```

## The UI/UX Tests (`ui_tests.py`)

```python
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
```

## Key Patterns in the UI/UX Tests

1. **Launch the Gradio app**: Use `demo.launch(prevent_thread_lock=True)` to get the URL
2. **Start Playwright**: Use `sync_playwright()` context manager
3. **Navigate to the app**: Use `page.goto(url)` to open the Gradio app
4. **Interact with components**: Use `page.get_by_label()`, `page.get_by_role()`, etc. to find and interact with UI elements
5. **Assert expectations**: Use Playwright's `expect()` API to verify the UI state
6. **Clean up**: Always close the browser and demo in a `finally` block

