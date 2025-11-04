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
        return "Error: Division by zero"
    return a / b

def square(a, b=None):
    """Square a number. Second parameter ignored."""
    return a * a

def calculate(operation, num1, num2):
    """Main calculation function that routes to appropriate operation."""
    try:
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
    except Exception as e:
        return f"Error: {str(e)}"

# Create Gradio interface
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
    
    # Example calculations
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