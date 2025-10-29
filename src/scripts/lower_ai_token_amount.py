import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))
from path_utils import get_chat_agent_data_dir

def remove_vowels(text):
    vowels = "AEIOUaeiou"
    result = ''.join([char for char in text if char not in vowels])
    return result

def process_files(input_file, output_file):
    try:
        # Read the input text from input.txt
        with open(input_file, 'r') as file:
            input_text = file.read()

        # Remove vowels from the input text
        result_text = remove_vowels(input_text)

        # Write the result to output.txt
        with open(output_file, 'w') as file:
            file.write(result_text)

        print(f"Processed text has been written to {output_file}")
    except FileNotFoundError:
        print(f"Error: The file {input_file} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Define the input and output file paths
input_file_path = str(get_chat_agent_data_dir() / "knowledge_base.txt")
output_file_path = str(get_chat_agent_data_dir() / "knowledge_base.txt")

# Call the function to process the files
process_files(input_file_path, output_file_path)