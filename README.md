# Testing Gradio Apps ⚒️

This repository demonstrates how to properly test Gradio applications using backend unit tests and, in particular, **UI/UX testing with Playwright**.

## Why Test Gradio Apps?

When building Gradio apps, you should test both the:

1. **Backend Functions** - Test your core logic with regular Python unit tests
2. **UI/UX** - Test the user interface and user interactions with the Gradio web app.

## Testing Backend Functions

Use standard Python testing frameworks like `pytest` or `unittest` to test your core functions independently of the Gradio interface.

```python
def test_add_function():
    assert add(2, 3) == 5
```

This is pretty standard and you probably already know how to do this (otherwise, [check out this tutorial](https://realpython.com/pytest-python-testing/)). The rest of this repo will focus on testing the Gradio UI.

## Testing the UI/UX

For user interface and user interaction testing, use **Playwright** (which has a **python API**) to:
- Launch your Gradio app
- Interact with UI components (inputs, buttons, etc.)
- Verify that the UI updates as expected

**Why Playwright for testing your Gradio apps?**

1. **Playwright has Python API**: Write tests entirely in Python
2. **Fits great with Gradio**: Works seamlessly with Gradio's web interface 
3. **Playwright's test generator**: Playwright's Test Generator can automatically write tests by recording your interactions

### Basic Playwright Test Flow

1. Start your Gradio app
2. Navigate to the app URL
3. Fill inputs, click buttons, etc.
4. Assert expected outputs appear

```python
def test_calculator_ui():
    with gr.Blocks() as demo:
        # your gradio app
        pass

    _, url, _, = demo.launch(prevent_thread_lock=True)

    # launch playwright on that url
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(url)
    
    page.fill("[data-testid='number1']", "5")
    page.fill("[data-testid='number2']", "3")
    page.click("text=Add")
    expect(page.locator("[data-testid='result']")).to_contain_text("8")

    demo.close()
```

## Example App & Testing

This repo includes a complete, simple Gradio app as well as the backend and UI/UX tests for that app. First, clone this repo and install the requirements.

#### Installation

1. Clone this repo:

```bash
git clone https://github.com/gradio-app/testing-gradio-apps.git
cd testing-gradio-apps
```

2. Install the requirements

```
pip install -r requirements.txt
```



This repo includes `app.py` - a simple calculator with two numeric inputs and a few simple operations:
- Add
- Subtract  
- Multiply
- Divide
- Square

You can run the Gradio web app with: `python app.py`.

If you use in this calculator, you will see the following expected behavior:

* If you click on "Square", the second numeric input disappears
* If you try to Divide by 0, you get an error
* Otherwise, behaves like a standard calculator by performing the requested operation when clicking the submit button.

#### Backend Testing

The backend tests are located in `backend_tests.py` and are just standard `pytest` unit tests. You can run the backend test by running `pytest backend_tests.py`.

#### UI/UX Testing

The UI/UX Playwright test file (called `ui_tests.py`) tests the expected behavior described above. 

* You can run the Playwright tests by running `pytest ui_tests.py`.


**Tip:** Instead of writing the Playwright tests manually, you can use Playwright's codegen tool to record your interactions and generate test code automatically:

```bash
playwright codegen localhost:7860
```