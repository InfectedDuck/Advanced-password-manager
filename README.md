# Password Manager with Enhanced Security

This project is a **Password Manager Application** built using **KivyMD**. It allows users to securely store and retrieve passwords, leveraging **encryption** for password safety. Additionally, it provides enhanced security features like **biometric authentication**, **two-factor authentication (2FA)** using SMS or email, and **TOTP-based authentication**.

## Features

### 1. **Password Management**
- Add, retrieve, and store passwords securely.
- Encrypts passwords using **Fernet encryption** from the `cryptography` library.
- Data is stored in a JSON file (`passwords.json`), and encryption keys are managed through a secure key file (`key.key`).

### 2. **Biometric Authentication**
- The app uses **facial recognition** as an added security layer.
- Utilizes the `face_recognition` and `cv2` libraries for face detection and matching against stored facial encodings.
- If biometric authentication fails, the user cannot access the password data.

### 3. **Two-Factor Authentication (2FA)**
- Provides **2FA via SMS** or **email**.
- Uses **Twilio** for sending SMS verification codes and **SMTP** for email-based verification.
- The code is sent to the user's registered email or phone number, and they must input the code to complete the authentication.

### 4. **TOTP-Based Authentication**
- Utilizes **Time-based One-Time Password (TOTP)** authentication with the `pyotp` library.
- A QR code is generated for the user to scan with an authenticator app like **Google Authenticator** or **Authy**.
- Verifies the TOTP entered by the user, ensuring time-based secure access.

## How to Run

1. **Install Dependencies**:
    Ensure you have Python installed, then install the required dependencies:
    ```bash
    pip install kivymd cryptography face_recognition pyotp twilio qrcode opencv-python
    ```

2. **Run the Application**:
    To launch the password manager:
    ```bash
    python main.py
    ```

3. **Security Features**:
    - Facial recognition requires a camera.
    - Ensure valid credentials are provided for **Twilio** and **SMTP** in the `send_code_via_sms_or_email` method for 2FA.
    - Scan the **TOTP QR code** with an authenticator app for secure time-based logins.

## Dependencies

- **KivyMD** for the UI components.
- **cryptography** for password encryption.
- **face_recognition** for biometric facial recognition.
- **pyotp** for TOTP authentication.
- **Twilio** for SMS-based two-factor authentication.
- **qrcode** for generating the QR code for TOTP.
- **OpenCV** for capturing images from the camera.

## Future Improvements

- Implementing recovery mechanisms for lost encryption keys.
- Adding more biometric authentication methods like fingerprint scanning.
- Storing encrypted data in a more secure, cloud-based solution.

## License

This project is licensed under the [Apache License 2.0](https://www.apache.org/licenses/LICENSE-2.0). See the [LICENSE](LICENSE.txt) file for details.
