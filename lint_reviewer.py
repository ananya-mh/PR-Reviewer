import subprocess
import shutil

def pylint_review(filepath):
#         result = subprocess.run(
#             ['pylint', filepath],
#             stdout=subprocess.PIPE,
#             stderr=subprocess.PIPE,
#             text=True,
#             check=True
#         )
#         return result.stdout

# print(f"Running pylint on: {filepath}")

    # Check if pylint is available
    pylint_path = shutil.which('pylint')
    if not pylint_path:
        print("Error: 'pylint' is not installed or not in PATH.")
        return "Pylint not found"

    try:
        result = subprocess.run(
            ['pylint', filepath],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )

        print("✅ Pylint ran successfully.")
        # print("🔍 STDOUT:\n", result.stdout)
        # print("❗ STDERR (if any):\n", result.stderr)
        
        return result.stdout + '\n' + result.stderr

    except subprocess.CalledProcessError as e:
        print(f"❌ Pylint process failed with error:\n{e.stderr}")
        return f"Pylint failed: {e.stderr}"

    except Exception as e:
        print(f"⚠️ Unexpected error while running pylint: {e}")
        return f"Unexpected error: {str(e)}"
    
    # except FileNotFoundError:
    #         print("Error: pylint is not installed or not in PATH.")
    # except subprocess.CalledProcessError as e:
    #         print(f"Pylint failed: {e.stderr}")
    # except Exception as e:
    #         print(f"Unexpected error while running pylint: {e}")
