"""
This script loads a Kiwix library XML file, sorts the <book> elements
by their 'path' attribute, and saves the sorted XML to a new file.
It uses Python's built-in xml.etree.ElementTree for XML parsing
and manipulation.

It also includes a verification function to ensure that all book IDs
from the input file are present in the output file and to warn about
any duplicate book IDs in the input file.
"""

import xml.etree.ElementTree as ET
import re
from collections import Counter

def sort_library_by_path(input_filepath: str, output_filepath: str):
    """
    Loads an XML file, sorts the <book> elements by their 'path' attribute,
    and saves the sorted XML to a new file.

    Args:
        input_filepath (str): The absolute or relative path to the input XML file.
        output_filepath (str): The absolute or relative path where the sorted XML will be saved.
    """
    try:
        # Parse the XML file
        tree = ET.parse(input_filepath)
        root = tree.getroot()

        # Find all 'book' elements directly under the root
        books = root.findall('book')

        # Sort the 'book' elements based on their 'path' attribute.
        # The 'key' argument uses a lambda function to extract the 'path' attribute
        # for each book. If 'path' is missing, an empty string is used to avoid errors.
        sorted_books = sorted(books, key=lambda book: book.get('path', ''))

        # Clear existing 'book' elements from the root to prepare for re-insertion
        for book in books:
            root.remove(book)

        # Append the newly sorted 'book' elements back to the root
        for book in sorted_books:
            root.append(book)

        # Create a new ElementTree object from the modified root
        sorted_tree = ET.ElementTree(root)

        # Save the sorted XML to the output file with UTF-8 encoding
        # and an XML declaration.
        sorted_tree.write(output_filepath, encoding='utf-8', xml_declaration=True)
        print(f"✅ Successfully sorted '{input_filepath}' and saved to '{output_filepath}'")
        return True

    except FileNotFoundError:
        print(f"❌ Error: The input file '{input_filepath}' was not found.")
    except ET.ParseError as e:
        print(f"❌ Error parsing XML file '{input_filepath}': {e}")
    except Exception as e:
        print(f"❌ An unexpected error occurred during sorting: {e}")
    return False

def verify_book_ids(input_filepath: str, output_filepath: str):
    """
    Verifies that every book ID from the input file is present in the output file.
    Also warns if duplicate book IDs are found in the input file.

    This function uses a regular expression to find all book IDs in the input
    and simple text searching to confirm their presence in the output. This serves
    as a robust, independent check on the transformation process.

    Args:
        input_filepath (str): The path to the original input XML file.
        output_filepath (str): The path to the processed output XML file.
    """
    print("\n--- Starting Verification ---")
    try:
        # 1. Read the input file and extract all book IDs using regex.
        with open(input_filepath, 'r', encoding='utf-8') as f:
            input_content = f.read()
        
        # This list will contain all occurrences of book IDs, including duplicates.
        all_input_ids = re.findall(r'book id="([^"]+)"', input_content)

        if not all_input_ids:
            print("⚠️ Warning: No book IDs found in the input file.")
            return

        # Using a set to get the unique IDs for verification.
        unique_input_ids = set(all_input_ids)

        # 2. Check for and warn about duplicates in the input file.
        if len(all_input_ids) > len(unique_input_ids):
            print(f"⚠️ Warning: Duplicate book IDs were found in '{input_filepath}'.")
            counts = Counter(all_input_ids)
            duplicates = {item: count for item, count in counts.items() if count > 1}
            print("   Duplicate IDs and their counts:")
            for item, count in duplicates.items():
                print(f"     - ID: {item}, Count: {count}")

        print(f"Found {len(unique_input_ids)} unique book IDs in '{input_filepath}'.")

        # 3. Read the entire output file into a string for searching.
        with open(output_filepath, 'r', encoding='utf-8') as f:
            output_content = f.read()

        # 4. Check for each unique input ID in the output file.
        missing_ids = []
        for book_id in unique_input_ids:
            # We search for the specific pattern 'id="..."' to avoid false positives
            # where the ID might appear as plain text elsewhere.
            search_pattern = f'id="{book_id}"'
            if search_pattern not in output_content:
                missing_ids.append(book_id)

        # 5. Report the results.
        if not missing_ids:
            print(f"✅ Verification successful: All {len(unique_input_ids)} unique book IDs are present in '{output_filepath}'.")
        else:
            print(f"❌ Verification FAILED: {len(missing_ids)} book ID(s) are missing from the output file.")
            print("Missing IDs:")
            for mid in missing_ids:
                print(f"  - {mid}")

    except FileNotFoundError as e:
        print(f"❌ Error: Could not find a file for verification: {e.filename}")
    except Exception as e:
        print(f"❌ An unexpected error occurred during verification: {e}")


if __name__ == "__main__":
    # Define input and output file paths.
    # The script will look for 'library.xml' in the same directory where it's executed,
    # and 'library_sorted.xml' will be created in that same directory.
    input_library_file = 'library.xml'
    output_sorted_file = 'library_sorted.xml'

    # Execute the sorting function
    success = sort_library_by_path(input_library_file, output_sorted_file)

    # If sorting was successful, run the verification check.
    if success:
        verify_book_ids(input_library_file, output_sorted_file)
