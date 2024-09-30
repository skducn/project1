# coding=utf-8
#***************************************************************
# Author     : John
# Created on : 2024-9-30
# Description: customtkinter
# http://www.51testing.com/?action-viewnews-itemid-7802825
#***************************************************************


import customtkinter as ctk

# Initial configuration
ctk.set_appearance_mode("dark")  # Set appearance mode: system, light, dark
ctk.set_default_color_theme("dark-blue")  # Set color theme: blue, dark-blue, green

# Create the main window
root = ctk.CTk()
root.geometry("500x350")  # Set the window size
root.title("Login System")  # Set the window title

# Example login function
def login():
    print("Login Successful")  # Placeholder function to simulate login

# Create the main frame
frame = ctk.CTkFrame(master=root)
frame.pack(pady=20, padx=60, fill="both", expand=True)  # Add frame with padding and expansion

# Create components
label = ctk.CTkLabel(master=frame, text="Login System", font=("Roboto", 24))
label.pack(pady=12, padx=10)  # Add a label with text and font settings
entry_username = ctk.CTkEntry(master=frame, placeholder_text="Username")
entry_username.pack(pady=12, padx=10)  # Add a username entry field with placeholder text
entry_password = ctk.CTkEntry(master=frame, placeholder_text="Password", show="*")
entry_password.pack(pady=12, padx=10)  # Add a password entry field with placeholder text and masked input
button = ctk.CTkButton(master=frame, text="Login", command=login)
button.pack(pady=12, padx=10)  # Add a login button and link it to the login function
checkbox = ctk.CTkCheckBox(master=frame, text="Remember Me")
checkbox.pack(pady=12, padx=10)  # Add a "Remember Me" checkbox
# Start the main loop
root.mainloop()  # Run the GUI application