import random
import pyotp
import qrcode
import smtplib
from twilio.rest import Client
import face_recognition
import cv2

known_face_images=["C:\Users\Admin\Pictures\Camera Roll\me.jpg"]
def biometric_authentication(known_face_images):
    def load_known_faces(known_face_images):
        known_faces = []
        for image_path in known_face_images:
            image = face_recognition.load_image_file(image_path)
            encoding = face_recognition.face_encodings(image)[0]
            known_faces.append(encoding)
        return known_faces

    def capture_image_from_camera():
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            print("Error: Could not open camera.")
            return None
        
        print("Please position yourself in front of the camera...")
        ret, frame = cap.read()

        if ret:
            cv2.imshow("Captured Image", frame)
            cv2.waitKey(2000) 
            cv2.destroyAllWindows()
            cap.release()
            return frame
        else:
            print("Error: Could not capture image.")
            cap.release()
            return None

    def recognize_faces_in_image(test_image, known_faces):
        rgb_frame = cv2.cvtColor(test_image, cv2.COLOR_BGR2RGB)
        test_encodings = face_recognition.face_encodings(rgb_frame)
        for test_encoding in test_encodings:
            results = face_recognition.compare_faces(known_faces, test_encoding)
            if True in results:
                return True
        return False

    print("Biometric authentication:")
    known_faces = load_known_faces(known_face_images)
    captured_image = capture_image_from_camera()
    if captured_image is None:
        print("Biometric authentication failed due to camera error.")
        return False
    print("Scanning face...")
    success = recognize_faces_in_image(captured_image, known_faces)
    
    if success:
        print("Biometric authentication successful!")
    else:
        print("Biometric authentication failed!")
    
    return success
def send_code_via_sms_or_email(method="sms"):
    code = random.randint(100000, 999999)
    if method == "email":
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login("toktarkametaj@gmail.com", "Kametaytoktar2023!!")
        message = f"Your verification code is {code}"
        server.sendmail("toktarkametaj@gmail.com", "kametaytoktar@gmail.com", message)
        server.quit()
    elif method == "sms":
        client = Client("AC195947051d789d8ffed97802281ec632", "4fee6f2e0b3363ff08c2dd1db4612d8a")
        message = client.messages.create(
            body=f"Your verification code is {code}",
            from_='+19127711098',
            to='+77072953027'
        )
    return code

def totp_authentication():
    secret = pyotp.random_base32()
    totp = pyotp.TOTP(secret)
    uri = totp.provisioning_uri("username@service", issuer_name="Your Service Name")
    qr = qrcode.make(uri)
    qr.show()
    
    user_input = input("Enter the OTP from your authenticator app: ")
    if totp.verify(user_input):
        print("TOTP authentication successful!")
        return True
    else:
        print("Invalid OTP")
        return False

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
