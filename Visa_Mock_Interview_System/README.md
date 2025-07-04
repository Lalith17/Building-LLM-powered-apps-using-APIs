# Visa Mock Interview System (VMIS) Utility

This Python script is a basic utility for the Visa Mock Interview System that processes user data, validates inputs, and prepares it for further processing.

## Features

1. **Input Validation**:

   - Validates names to contain only alphabets
   - Validates email format
   - Validates age is a positive integer

2. **User Classification**:

   - Underage: Below 18
   - Adult: Between 18 and 60
   - Senior: Above 60

3. **File Handling**:

   - Saves validated data to `user_data.txt`
   - Appends new entries without overwriting existing data

4. **Error Handling**:

   - Handles invalid data inputs
   - Manages file operations safely

5. **Logging**:

   - Logs validation errors and successful operations to `app_logs.txt`

6. **Menu-Driven Interface**:
   - Add new entries
   - View all saved entries
   - Exit the program

## How to Run

1. Ensure you have Python 3.x installed on your system.
2. Save the script as `vmis_utility.py`.
3. Run the script from the command line: `python vmis_utility.py`
4. Follow the on-screen menu options to interact with the program.

## Output Files

1. `user_data.txt`: Contains all successfully saved user entries.
2. `app_logs.txt`: Contains logs of program operations and errors.

## Testing

The `test_cases.txt` file contains sample inputs and expected outputs to verify the program's functionality.

## Notes

- The program will create the output files if they don't exist.
- Existing data in `user_data.txt` will not be overwritten; new entries are appended.
- Logs are written to both the console and `app_logs.txt`.
