def count_characters_in_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()  # Read the whole file into a string
            return len(content)    # Count the number of characters in the string
    except FileNotFoundError:
        return "The file does not exist"
    except Exception as e:
        return f"An error occurred: {e}"

# Example usage
file_path = '../data/jsons/Verifiable_Internet_for_Artificial_Intelligence_whitepaper.json'  # Adjust this to your file's location
character_count = count_characters_in_file(file_path)
print(f"The file contains {character_count} characters.")

