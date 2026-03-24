import subprocess
import tempfile


def run_code(user_code, test_input):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py") as f:
        f.write(user_code.encode())
        filename = f.name

    try:
        result = subprocess.run(
            ["python", filename],
            input=test_input,
            text=True,
            capture_output=True,
            timeout=3
        )
        return result.stdout.strip(), result.stderr
    except Exception as e:
        return None, str(e)