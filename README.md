# sort_kiwix_library
A Python script to sort a Kiwix library.xml file by book path and verify the result.

## Requirements

* Python 3

(No external libraries are required.)

## Usage

1.  **Place your library file:** Put your `library.xml` file in the same directory as the `sort_kiwix_library.py` script.

2.  **Run the script:** Open your terminal or command prompt, navigate to the directory, and run the script:
    ```bash
    python sort_kiwix_library.py
    ```

3.  **Find the output:** The script will process the input and create a new file named `library_sorted.xml` in the same directory. This file contains the sorted content.

## Verification

After a successful sort, the script automatically performs a verification check to:
* Confirm that all book IDs from `library.xml` are present in `library_sorted.xml`.
* Warn you if any duplicate book IDs were found in the original file.
