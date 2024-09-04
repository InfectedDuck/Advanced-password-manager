from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.button import MDRaisedButton, MDFlatButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import ScreenManager
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.gridlayout import MDGridLayout
from cryptography.fernet import Fernet
import json
import os

KEY_FILE = 'key.key'
DATA_FILE = 'passwords.json'

def load_key():
    if os.path.exists(KEY_FILE):
        with open(KEY_FILE, 'rb') as file:
            return Fernet(file.read())
    else:
        key = Fernet.generate_key()
        with open(KEY_FILE, 'wb') as file:
            file.write(key)
        return Fernet(key)

def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, 'r') as file:
            return json.load(file)
    return {}

def save_data(data):
    with open(DATA_FILE, 'w') as file:
        json.dump(data, file)

def encrypt_password(password):
    return fernet.encrypt(password.encode()).decode()

def decrypt_password(encrypted_password):
    return fernet.decrypt(encrypted_password.encode()).decode()

fernet = load_key()

class PasswordManagerScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = MDBoxLayout(orientation='vertical', padding=10, spacing=10)

        self.title_label = MDLabel(text="Password Manager", font_style="H4", halign="center")
        self.layout.add_widget(self.title_label)

        self.site_entry = MDTextField(hint_text="Site", mode="rectangle")
        self.layout.add_widget(self.site_entry)

        self.username_entry = MDTextField(hint_text="Username", mode="rectangle")
        self.layout.add_widget(self.username_entry)

        self.email_entry = MDTextField(hint_text="Email", mode="rectangle")
        self.layout.add_widget(self.email_entry)

        self.password_entry = MDTextField(hint_text="Password", password=True, mode="rectangle")
        self.layout.add_widget(self.password_entry)

        self.add_button = MDRaisedButton(text="Add Password", on_release=self.add_password)
        self.show_button = MDRaisedButton(text="Show All Passwords", on_release=self.show_passwords)
        self.layout.add_widget(self.add_button)
        self.layout.add_widget(self.show_button)

        self.add_widget(self.layout)

    def add_password(self, instance):
        site = self.site_entry.text
        username = self.username_entry.text
        email = self.email_entry.text
        password = self.password_entry.text

        if not site or not username or not email or not password:
            self.show_popup("Error", "All fields are required!")
            return

        data = load_data()
        encrypted_password = encrypt_password(password)
        data[site] = {"username": username, "email": email, "password": encrypted_password}
        save_data(data)

        self.site_entry.text = ""
        self.username_entry.text = ""
        self.email_entry.text = ""
        self.password_entry.text = ""
        self.show_popup("Success", "Password added successfully!")

    def show_passwords(self, instance):
        data = load_data()
        if not data:
            self.show_popup("Info", "No passwords saved.")
            return

        grid = MDGridLayout(cols=1, spacing=10, size_hint_y=None)
        grid.bind(minimum_height=grid.setter('height'))

        for site, info in data.items():
            decrypted_password = decrypt_password(info["password"])
            grid.add_widget(MDLabel(text=f"Site: {site}", size_hint_y=None, height=40))
            grid.add_widget(MDLabel(text=f"Username: {info['username']}", size_hint_y=None, height=40))
            grid.add_widget(MDLabel(text=f"Email: {info['email']}", size_hint_y=None, height=40))
            grid.add_widget(MDLabel(text=f"Password: {decrypted_password}", size_hint_y=None, height=40))
            grid.add_widget(MDLabel(text="", size_hint_y=None, height=10))

        scroll_view = MDScrollView()
        scroll_view.add_widget(grid)
        self.add_widget(scroll_view)

    def show_popup(self, title, message):
        self.dialog = MDDialog(
            title=title,
            text=message,
            buttons=[MDFlatButton(text="OK", on_release=self.close_dialog)],
        )
        self.dialog.open()

    def close_dialog(self, instance):
        self.dialog.dismiss()

class PasswordManagerApp(MDApp):
    def build(self):
        sm = ScreenManager()
        sm.add_widget(PasswordManagerScreen(name='password_manager'))
        return sm

if __name__ == "__main__":
    PasswordManagerApp().run()
