import sys
import io


def execute_user_code(code):
    """Executes the given Python code and returns the output.

    Args:
      code: A string containing the Python code to execute.

    Returns:
      A string containing the output of the code, or an error message.
    """

    # Capture stdout and stderr to get the output
    old_stdout = sys.stdout
    sys.stdout = buffer = io.StringIO()

    try:
        # Execute the code using exec()
        exec(code)
    except Exception as e:
        return f"Error: {e}"
    finally:
        # Restore stdout
        sys.stdout = old_stdout

    # Return the captured output
    return buffer.getvalue()


if __name__ == "__main__":
    user_code = input("Enter your Python code:\n")
    output = execute_user_code(user_code)
    print("Output:\n", output)
