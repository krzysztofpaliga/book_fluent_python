import os
import readline
import code
import sys
import shutil
import atexit
from io import StringIO

# File paths for the session and temporary files
histfile = os.path.join(os.getcwd(), "repl-session.py")
tempfile = os.path.join(os.getcwd(), "repl-session.tmp")

# Initialize the InteractiveConsole
console = code.InteractiveConsole(globals())

# Function to save input/output to the temporary file during REPL session


def get_multiline_input():
    lines = []
    prompt = ">>> "
    while True:
        line = input(prompt)
        lines.append(line)
        if line.endswith(":"):
            prompt = "... "
        elif len(lines) > 1 and line.strip() == "":
            break
        elif len(lines) == 1:
            break
    return "\n".join(lines)


def save_input_output_temp(input_data, output_data):
    with open(tempfile, 'a') as f:
        # Save the input as it would be typed in the REPL (without '>>>')
        if input_data.strip() != "":  # Only save non-empty lines
            f.write(f"{input_data}\n")

        f.write("#\n")

        # Save the output as comments if it's not empty
        if output_data.strip():
            for line in output_data.strip().splitlines():
                f.write(f"# {line}\n")

# Custom function to capture the output of the REPL


def custom_exec_input(input_data):
    output_buffer = StringIO()
    original_stdout = sys.stdout
    sys.stdout = output_buffer
    try:
        console.push(input_data)
        output_data = output_buffer.getvalue()
    except Exception as e:
        output_data = f"Error: {e}"
    sys.stdout = original_stdout
    return output_data

# Function to load a file into the REPL and execute its contents


def load_file_to_repl_multiline(file_name):
    if os.path.exists(file_name):
        with open(file_name, 'r') as file:
            buffer = []
            in_multiline = False

            for line in file:
                line = line.rstrip()

                if not in_multiline:
                    buffer.append(line)
                    in_multiline = line.endswith(":")
                    if not in_multiline:
                        custom_exec_input("\n".join(buffer))
                        buffer = []
                        continue
                else:
                    if line.startswith("#"):
                        buffer.append("")
                        in_multiline = False
                        break
                    else:
                        buffer.append(f"{line}")
                        continue

            # Final flush if any buffer remains
            if buffer:
                custom_exec_input("\n".join(buffer))
                buffer = []


def load_file_to_repl(file_name):
    if os.path.exists(file_name):
        with open(file_name, 'r') as file:
            for line in file:
                line = line.rstrip()  # Ensure there are no trailing spaces
                # Ignore empty comment lines
                if line and not line.startswith("#"):
                    custom_exec_input(line)  # Execute the line in REPL

# Function to replace the session file with the temporary file


def finalize_session():
    # Make sure the session file is removed before replacing it
    if os.path.exists(histfile):
        os.remove(histfile)  # Remove the old session file if it exists

    # Now move the temporary file to replace the session file
    shutil.move(tempfile, histfile)


# Register finalize_session to run on exit
atexit.register(finalize_session)

# Main REPL loop


def start_repl():
    # If session file exists, copy it to the temporary file first
    if os.path.exists(histfile):
        # Copy the current session to the temp file
        shutil.copy(histfile, tempfile)

    # Load the previous session's input and execute it (but don't save during loading)
    if os.path.exists(histfile):
        load_file_to_repl_multiline(histfile)

    while True:
        try:
            user_input = get_multiline_input()
            if user_input.lower() in ['exit', 'quit']:
                break
            output_data = custom_exec_input(user_input)
            if output_data:
                print(output_data, end="")  # Print output to console
            # Save input/output to the temporary file immediately
            save_input_output_temp(user_input, output_data)
        except Exception as e:
            print(f"Error: {e}")
        except KeyboardInterrupt:
            print("\nKeyboardInterrupt")
        except EOFError:
            print("\nEOF received, exiting...")
            break


# Start the REPL
start_repl()
