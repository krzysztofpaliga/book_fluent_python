import os
import readline
import code
import sys
from io import StringIO

# File to store history (input/output)
histfile = os.path.expanduser("repl-session.py")

# Initialize the InteractiveConsole
console = code.InteractiveConsole(globals())

# Function to save input/output to history file in a REPL-compatible format
def save_input_output(input_data, output_data):
    with open(histfile, 'a') as f:
        # Save the input as it would be typed in the REPL (without '>>>')
        f.write(f"{input_data}\n")

        # Save the output if it's not empty (as Python code format, as comments)
        if output_data.strip():  # If output is not empty
            # Split the output by lines and write each line with a comment marker
            for line in output_data.splitlines():
                f.write(f"# {line}\n")  # Mark output as a Python comment

# Custom function to capture the output of the REPL
def custom_exec_input(input_data):
    # Use StringIO to capture the output
    output_buffer = StringIO()

    # Backup the original stdout
    original_stdout = sys.stdout
    sys.stdout = output_buffer  # Redirect stdout to the StringIO buffer

    try:
        # Execute the input in the REPL
        result = console.push(input_data)
        output_data = output_buffer.getvalue()  # Capture the output from StringIO buffer
    except Exception as e:
        output_data = f"Error: {e}"

    # Restore the original stdout
    sys.stdout = original_stdout
    return output_data

# Function to load a file into the REPL and save it to history
def load_file_to_repl(file_name):
    if os.path.exists(file_name):
        with open(file_name, 'r') as file:
            for line in file:
                # Save the input (file contents) to history
                save_input_output(line.strip(), "")
                # Execute each line in the REPL
                custom_exec_input(line.strip())

# Function to start REPL loop
def start_repl():
    # Check if a file was passed as a parameter and load it into the REPL
    if len(sys.argv) > 1:
        file_name = sys.argv[1]
        load_file_to_repl(file_name)
    
    # Start interactive REPL
    while True:
        try:
            # Get input from the user
            user_input = input(">>> ")
            if user_input.lower() in ['exit', 'quit']:
                break  # Exit REPL when "exit" or "quit" is typed

            # Call the custom execution to capture output
            output_data = custom_exec_input(user_input)

            # Print the output to the terminal (stdout)
            if output_data:
                print(output_data, end="")  # Directly print to terminal

            # Save the input (always) and output (only if non-empty)
            save_input_output(user_input, output_data)

        except Exception as e:
            print(f"Error: {e}")

# Start the REPL loop
start_repl()

