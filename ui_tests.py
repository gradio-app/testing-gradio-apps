import pytest
import gradio as gr
from playwright.sync_api import sync_playwright, expect
import threading
import time
from app import demo

def test_calculator_basic_operations():
    """Test basic calculator operations through the UI."""
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