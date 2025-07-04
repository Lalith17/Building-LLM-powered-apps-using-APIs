import re
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app_logs.txt'),
        logging.StreamHandler()
    ]
)

def validate_name(name):
    """Validate that the name contains only alphabets and spaces."""
    if not name.replace(' ', '').isalpha():
        logging.error(f"Invalid name: {name}. Names must contain only alphabets.")
        return False
    return True

def validate_email(email):
    """Validate the email format using regular expression."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, email):
        logging.error(f"Invalid email: {email}. Please enter a valid email address.")
        return False
    return True

def validate_age(age_str):
    """Validate that age is a positive integer."""
    try:
        age = int(age_str)
        if age <= 0:
            logging.error(f"Invalid age: {age}. Age must be a positive integer.")
            return False
        return True
    except ValueError:
        logging.error(f"Invalid age input: {age_str}. Age must be a number.")
        return False

def classify_age(age):
    """Classify the user based on their age."""
    age = int(age)
    if age < 18:
        return "Underage"
    elif 18 <= age <= 60:
        return "Adult"
    else:
        return "Senior"

def save_user_data(name, email, age, category):
    """Save validated user data to a file."""
    try:
        with open('user_data.txt', 'a') as file:
            entry = f"Name: {name}, Email: {email}, Age: {age}, Category: {category}\n"
            file.write(entry)
        logging.info(f"Successfully saved user data: {name}")
    except IOError as e:
        logging.error(f"Error writing to file: {e}")

def view_all_entries():
    """Display all saved user entries."""
    try:
        with open('user_data.txt', 'r') as file:
            entries = file.readlines()
            if not entries:
                print("No user entries found.")
            else:
                print("\n=== Saved User Entries ===")
                for entry in entries:
                    print(entry.strip())
    except FileNotFoundError:
        print("No user data file found. Please add entries first.")
        logging.warning("Attempted to view entries but user_data.txt not found.")

def main_menu():
    """Display the main menu and handle user choices."""
    while True:
        print("\nVisa Mock Interview System (VMIS) Utility")
        print("1. Add new entry")
        print("2. View all entries")
        print("3. Exit")
        
        choice = input("Please select an option (1-3): ")
        
        if choice == '1':
            add_new_entry()
        elif choice == '2':
            view_all_entries()
        elif choice == '3':
            print("Exiting the program. Goodbye!")
            logging.info("Program exited by user.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 3.")
            logging.warning(f"Invalid menu choice entered: {choice}")

def add_new_entry():
    """Collect and validate user data."""
    print("\n=== Add New User Entry ===")
    
    # Get and validate name
    while True:
        name = input("Enter your full name: ").strip()
        if validate_name(name):
            break
    
    # Get and validate email
    while True:
        email = input("Enter your email: ").strip()
        if validate_email(email):
            break
    
    # Get and validate age
    while True:
        age = input("Enter your age: ").strip()
        if validate_age(age):
            break
    
    # Classify user
    category = classify_age(age)
    
    # Save data
    save_user_data(name, email, age, category)
    
    # Display success message
    print("\nUser data successfully saved!")
    print(f"Name: {name}")
    print(f"Email: {email}")
    print(f"Age: {age}")
    print(f"Category: {category}")

if __name__ == "__main__":
    logging.info("Program started.")
    main_menu()