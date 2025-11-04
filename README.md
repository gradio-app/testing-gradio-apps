# Testing Gradio Apps

This repository demonstrates how to properly test Gradio applications using both backend unit tests and UI testing with Playwright.

## Why Test Gradio Apps?

When building Gradio apps, you should test both:

1. **Backend Functions** - Test your core logic with regular Python unit tests
2. **Gradio UI** - Test the user interface and interactions

## Testing Backend Functions

Use standard Python testing frameworks like `pytest` or `unittest` to test your core functions independently of the Gradio interface.

```python
def test_add_function():
    assert add(2, 3) == 5
```

## Testing the Gradio UI

For UI testing, use **Playwright** (which has a **python API**) to:
- Launch your Gradio app
- Interact with UI components (inputs, buttons, etc.)
- Verify that the UI changes as expected

**Why Playwright for testing your Gradio apps?**

1. **Playwright has Python API**: Write tests entirely in Python
2. **Fits great with Gradio**: Works seamlessly with Gradio's web interface 
3. **Playwright's test generator**: Playwright's Test Generator can automatically write tests by recording your interactions

### Basic Playwright Test Flow

1. Start your Gradio app
2. Navigate to the app URL
3. Fill inputs, click buttons
4. Assert expected outputs appear

```python
def test_calculator_ui():
    # Launch Gradio app
    with gr.Blocks() as demo:
        # Your app code
        pass
    
    # Use Playwright to test the UI
    page.fill("[data-testid='number1']", "5")
    page.fill("[data-testid='number2']", "3")
    page.click("text=Add")
    expect(page.locator("[data-testid='result']")).to_contain_text("8")
```

## Getting Started

1. Install dependencies:
   ```bash
   pip install gradio pytest playwright
   playwright install
   ```

2. Run the app:
   ```bash
   python app.py
   ```

3. Run tests:
   ```bash
   pytest tests/
   ```

## Example App

This repo includes `app.py` - a simple calculator with operations:
- Add
- Subtract  
- Multiply
- Divide
- Square

The calculator demonstrates both backend function testing and UI testing patterns.