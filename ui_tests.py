import pytest
import gradio as gr
from playwright.sync_api import sync_playwright, expect
import threading
import time
from app import add, subtract, multiply, divide, square, calculate

def test_calculator_basic_operations():
    """Test basic calculator operations through the UI."""
    with gr.Blocks(title="Calculator App") as demo:
        gr.Markdown("# Simple Calculator")
        gr.Markdown("Choose an operation and enter numbers to calculate.")
        
        with gr.Row():
            operation = gr.Dropdown(
                choices=["Add", "Subtract", "Multiply", "Divide", "Square"],
                label="Operation",
                value="Add"
            )
        
        with gr.Row():
            num1 = gr.Number(label="First Number", value=0)
            num2 = gr.Number(label="Second Number (ignored for Square)", value=0)
        
        calculate_btn = gr.Button("Calculate", variant="primary")
        result = gr.Textbox(label="Result", interactive=False)
        
        def update_visibility(operation):
            if operation == "Square":
                return gr.update(visible=False)
            else:
                return gr.update(visible=True)
        
        operation.change(
            fn=update_visibility,
            inputs=operation,
            outputs=num2
        )
        
        calculate_btn.click(
            fn=calculate,
            inputs=[operation, num1, num2],
            outputs=result
        )

    # Launch the demo
    _, url, _ = demo.launch(prevent_thread_lock=True)
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url)
            
            # Wait for page to load
            page.wait_for_selector("button:has-text('Calculate')")
            
            # Test Addition
            page.locator("input[aria-label='First Number']").fill("5")
            page.locator("input[aria-label='Second Number (ignored for Square)']").fill("3")
            page.click("button:has-text('Calculate')")
            
            # Wait for result and verify
            page.wait_for_timeout(1000)
            result_text = page.locator("textarea[aria-label='Result']").input_value()
            assert result_text == "8"
            
            browser.close()
    finally:
        demo.close()

def test_calculator_square_operation():
    """Test that second input disappears for Square operation."""
    with gr.Blocks(title="Calculator App") as demo:
        gr.Markdown("# Simple Calculator")
        gr.Markdown("Choose an operation and enter numbers to calculate.")
        
        with gr.Row():
            operation = gr.Dropdown(
                choices=["Add", "Subtract", "Multiply", "Divide", "Square"],
                label="Operation",
                value="Add"
            )
        
        with gr.Row():
            num1 = gr.Number(label="First Number", value=0)
            num2 = gr.Number(label="Second Number (ignored for Square)", value=0)
        
        calculate_btn = gr.Button("Calculate", variant="primary")
        result = gr.Textbox(label="Result", interactive=False)
        
        def update_visibility(operation):
            if operation == "Square":
                return gr.update(visible=False)
            else:
                return gr.update(visible=True)
        
        operation.change(
            fn=update_visibility,
            inputs=operation,
            outputs=num2
        )
        
        calculate_btn.click(
            fn=calculate,
            inputs=[operation, num1, num2],
            outputs=result
        )

    # Launch the demo
    _, url, _ = demo.launch(prevent_thread_lock=True)
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url)
            
            # Wait for page to load
            page.wait_for_selector("button:has-text('Calculate')")
            
            # Check that second input is visible initially
            second_input = page.locator("input[aria-label='Second Number (ignored for Square)']")
            expect(second_input).to_be_visible()
            
            # Select Square operation
            page.click(".dropdown")
            page.click("text=Square")
            
            # Wait for UI update
            page.wait_for_timeout(1000)
            
            # Check that second input is now hidden
            expect(second_input).to_be_hidden()
            
            # Test square calculation
            page.locator("input[aria-label='First Number']").fill("4")
            page.click("button:has-text('Calculate')")
            
            # Wait for result and verify
            page.wait_for_timeout(1000)
            result_text = page.locator("textarea[aria-label='Result']").input_value()
            assert result_text == "16"
            
            browser.close()
    finally:
        demo.close()

def test_calculator_division_by_zero():
    """Test division by zero error handling."""
    with gr.Blocks(title="Calculator App") as demo:
        gr.Markdown("# Simple Calculator")
        gr.Markdown("Choose an operation and enter numbers to calculate.")
        
        with gr.Row():
            operation = gr.Dropdown(
                choices=["Add", "Subtract", "Multiply", "Divide", "Square"],
                label="Operation",
                value="Add"
            )
        
        with gr.Row():
            num1 = gr.Number(label="First Number", value=0)
            num2 = gr.Number(label="Second Number (ignored for Square)", value=0)
        
        calculate_btn = gr.Button("Calculate", variant="primary")
        result = gr.Textbox(label="Result", interactive=False)
        
        def update_visibility(operation):
            if operation == "Square":
                return gr.update(visible=False)
            else:
                return gr.update(visible=True)
        
        operation.change(
            fn=update_visibility,
            inputs=operation,
            outputs=num2
        )
        
        calculate_btn.click(
            fn=calculate,
            inputs=[operation, num1, num2],
            outputs=result
        )

    # Launch the demo
    _, url, _ = demo.launch(prevent_thread_lock=True)
    
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page()
            page.goto(url)
            
            # Wait for page to load
            page.wait_for_selector("button:has-text('Calculate')")
            
            # Select Divide operation
            page.click(".dropdown")
            page.click("text=Divide")
            
            # Test division by zero
            page.locator("input[aria-label='First Number']").fill("10")
            page.locator("input[aria-label='Second Number (ignored for Square)']").fill("0")
            page.click("button:has-text('Calculate')")
            
            # Wait for result and verify error message
            page.wait_for_timeout(1000)
            result_text = page.locator("textarea[aria-label='Result']").input_value()
            assert "Error: Division by zero" in result_text
            
            browser.close()
    finally:
        demo.close()