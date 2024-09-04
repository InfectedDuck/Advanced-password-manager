import subprocess
from security_part import biometric_authentication, send_code_via_sms_or_email, totp_authentication

def main():
    print("Choose your preferred authentication method:")
    print("1. Biometric Authentication")
    print("2. SMS Verification")
    print("3. Email Verification")
    print("4. TOTP (Time-Based One-Time Password)")

    choice = input("Enter your choice (1-4): ")
    
    if choice == '1':
        if biometric_authentication():
            print("Access granted!")
        else:
            print("Access denied!")
    elif choice == '2':
        code = send_code_via_sms_or_email(method="sms")
        user_input = input("Enter the code you received via SMS: ")
        if user_input == str(code):
            print("SMS verification successful!")
            print("Access granted!")
        else:
            print("Invalid code. Access denied!")
    elif choice == '3':
        code = send_code_via_sms_or_email(method="email")
        user_input = input("Enter the code you received via email: ")
        if user_input == str(code):
            print("Email verification successful!")
            print("Access granted!")
        else:
            print("Invalid code. Access denied!")
    elif choice == '4':
        if totp_authentication():
            print("Access granted!")
        else:
            print("Access denied!")
    else:
        print("Invalid choice. Please choose between 1 and 4.")

if __name__ == "__main__":
    main()