# Testing Gradio Apps ⚒️

This repository demonstrates how to test Gradio applications using backend unit tests and, in particular, **UI/UX tests with Playwright**.




https://github.com/user-attachments/assets/a2f4a8ba-b625-492f-a849-0b0b329d8ca9







## Why kind of tests does your Gradio app need?

When building Gradio apps, you should test both the:

1. **Backend Functions** - Many Gradio apps contain Python backend functions that can be run independently of the UI. Test these with standard Python unit tests to ensure the core logic of your app works as expected.

Use standard Python testing frameworks like `pytest` or `unittest` to test your core functions independently of the Gradio interface.

```python
def test_add_function():
    assert add(2, 3) == 5
```

You probably already know how to do this (otherwise, [check out this tutorial](https://realpython.com/pytest-python-testing/)).


2. **UI/UX** - In addition, you should test the interface and interactions with the Gradio web app to ensure that users experience the Gradio app as you would expect. 

For user interface and user interaction testing, we recommend using **Playwright** (which has a **python API**) to:
- Launch your Gradio app
- Interact with UI components (inputs, buttons, etc.)
- Verify that the UI appears or updates as expected

## Why do we recommend Playwright?

1. **Playwright has Python API**: You can write your tests, including all of the web browser interactions, entirely in Python (just like your Gradio web app!).
2. **Playwright fits great with Gradio**: Playwright works out-of-the-box with Gradio, and in fact, we use Playwright within Gradio itself for our interaction tests.
3. **Playwright Codegen**: The best part is that Playwright comes with a Test Generator that can automatically write tests in Python by recording your interactions, as shown at the top of this README.

Here's what a typical interaction test written with Playwright will look like:

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

## Example app & tests

This repo includes a complete, simple Gradio calculator app as well as the backend and UI/UX tests for that app. First, clone this repo and install the requirements.

#### Installation

1. Clone this repo:

```bash
git clone https://github.com/gradio-app/testing-gradio-apps.git
cd testing-gradio-apps
```

2. Install the requirements

```bash
pip install -r requirements.txt
```

3. Install Playwright

```bash
playwright install
```

After you've run the commands above in your terminal (only need to do it once), then you are ready to run the Gradio app and the tests:

#### Gradio app

The example Gradio app in this repo is a simple calculator that can you can run by typing `python run.py` in your terminal.

#### Backend Testing

The backend tests are located in `backend_tests.py` and are just standard `pytest` unit tests. You can run the backend test by running `pytest backend_tests.py`.

#### UI/UX Testing

The UI/UX Playwright test file (called `ui_tests.py`) tests the expected behavior described above. 

* You can run the Playwright tests by running `pytest ui_tests.py`.


## Exercise for the reader

Now that you know how to set up and run the interaction tests, **we recommend you write 1 more interaction test for the calculator app**. As mentioned earlier, instead of writing the Playwright tests manually, you can use Playwright's codegen tool to record your interactions and generate test code automatically:

```bash
python app.py
```

and then in another terminal (assuming the Gradio app launches on port 7860):

```bash
playwright codegen localhost:7860
```

## For LLMs

If you'd like to an LLM to generate tests for you, I recommend providing an example Gradio app & the Playwright tests for that Gradio app so that they understand what the syntax should be. [This Markdown file](example-app-and-tests.md) contains the example Gradio calculator app mentioned above and its associated UI/UX tests. In our experience, Playwright's Codegen tool works better than asking an LLM to write Playwright tests from scratch, but your mileage may vary!
