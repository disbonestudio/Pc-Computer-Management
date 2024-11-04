import tkinter as tk
from tkinter import ttk
import json
import os
from tkinter import messagebox
import customtkinter as ctk

# Define the path to the contacts file in the 'database' folder
DATABASE_FOLDER = "database"
CONTACTS_FILE = os.path.join(DATABASE_FOLDER, "contacts.json")

class PhoneBookApp:
    def __init__(self, app):
        # Create the 'database' folder if it doesn't exist
        if not os.path.exists(DATABASE_FOLDER):
            os.makedirs(DATABASE_FOLDER)

        # Initialize the UI components
        self.name_CTkLabel = ctk.CTkLabel(app, text="Name:")
        self.name_CTkLabel.grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.name_CTkEntry = ctk.CTkEntry(app)
        self.name_CTkEntry.grid(row=0, column=1, padx=5, pady=5)

        self.number_CTkLabel = ctk.CTkLabel(app, text="Phone Number:")
        self.number_CTkLabel.grid(row=1, column=0, padx=5, pady=5, sticky="w")
        self.number_CTkEntry = ctk.CTkEntry(app)
        self.number_CTkEntry.grid(row=1, column=1, padx=5, pady=5)

        self.add_CTkButton = ctk.CTkButton(app, text="Add Contact", command=self.add_contact)
        self.add_CTkButton.grid(row=2, column=0, pady=10)

        self.edit_CTkButton = ctk.CTkButton(app, text="Edit Contact", command=self.prepare_edit_contact)
        self.edit_CTkButton.grid(row=2, column=1, pady=10)

        self.delete_CTkButton = ctk.CTkButton(app, text="Delete Contact", command=self.delete_contact)
        self.delete_CTkButton.grid(row=2, column=2, pady=10)

        # Treeview for displaying contacts
        self.contact_tree = ttk.Treeview(app, columns=("ID", "Name", "Phone Number"), show="headings")
        self.contact_tree.heading("ID", text="ID")
        self.contact_tree.heading("Name", text="Name")
        self.contact_tree.heading("Phone Number", text="Phone Number")
        self.contact_tree.grid(row=3, column=0, columnspan=3, padx=5, pady=5)

        self.refresh_contacts()

        # Event handler for double-clicking on a contact
        self.contact_tree.bind("<Double-1>", self.prepare_edit_contact)

    def add_contact(self):
        name = self.name_CTkEntry.get()
        number = self.number_CTkEntry.get()

        if name and number:
            if not number.isdigit():
                messagebox.showwarning("Invalid Input", "Please enter a valid phone number.")
                return

            contact = {"id": self.generate_contact_id(), "name": name, "number": number}
            self.save_contact(contact)
            self.refresh_contacts()
            self.name_CTkEntry.delete(0, tk.END)
            self.number_CTkEntry.delete(0, tk.END)
        else:
            messagebox.showwarning("Incomplete Input", "Please enter both name and phone number.")

    def prepare_edit_contact(self, event=None):
        selected_item = self.contact_tree.selection()
        if not selected_item:
            messagebox.showinfo("Edit Contact", "Please select a contact to edit.")
            return

        contact_id = int(self.contact_tree.item(selected_item, "values")[0])
        contact = self.load_contact(contact_id)

        if contact:
            self.name_CTkEntry.delete(0, tk.END)
            self.name_CTkEntry.insert(0, contact["name"])
            self.number_CTkEntry.delete(0, tk.END)
            self.number_CTkEntry.insert(0, contact["number"])

        # Update button command to use 'configure' instead of 'config'
            self.edit_CTkButton.configure(command=lambda: self.edit_contact(contact_id))

            self.edit_CTkButton.configure(command=lambda: self.edit_contact(contact_id))


    def edit_contact(self, contact_id):
        name = self.name_CTkEntry.get()
        number = self.number_CTkEntry.get()

        if name and number:
            if not number.isdigit():
                    messagebox.showwarning("Invalid Input", "Please enter a valid phone number.")
                    return

            updated_contact = {"id": contact_id, "name": name, "number": number}
            self.update_contact(contact_id, updated_contact)
            self.refresh_contacts()
            self.name_CTkEntry.delete(0, tk.END)
            self.number_CTkEntry.delete(0, tk.END)
        
        # Update button command to use 'configure' instead of 'config'
            self.edit_CTkButton.configure(command=self.prepare_edit_contact)
        else:
            messagebox.showwarning("Incomplete Input", "Please enter both name and phone number.")

    def delete_contact(self):
        selected_item = self.contact_tree.selection()
        if not selected_item:
            messagebox.showinfo("Delete Contact", "Please select a contact to delete.")
            return

        confirmation = messagebox.askyesno("Delete Contact", "Are you sure you want to delete this contact?")
        if confirmation:
            contact_id = int(self.contact_tree.item(selected_item, "values")[0])
            self.remove_contact(contact_id)
            self.refresh_contacts()

    def refresh_contacts(self):
        # Clear existing data
        for row in self.contact_tree.get_children():
            self.contact_tree.delete(row)

        # Fetch data from JSON and display in the Treeview
        contacts = self.load_all_contacts()
        for contact in contacts:
            self.contact_tree.insert("", "end", values=(contact["id"], contact["name"], contact["number"]))

    def generate_contact_id(self):
        contacts = self.load_all_contacts()
        if contacts:
            return max(contact["id"] for contact in contacts) + 1
        return 1

    def save_contact(self, contact):
        contacts = self.load_all_contacts()
        contacts.append(contact)
        self.save_all_contacts(contacts)

    def load_contact(self, contact_id):
        contacts = self.load_all_contacts()
        for contact in contacts:
            if contact["id"] == contact_id:
                return contact
        return None

    def update_contact(self, contact_id, updated_contact):
        contacts = self.load_all_contacts()
        for i, contact in enumerate(contacts):
            if contact["id"] == contact_id:
                contacts[i] = updated_contact
                break
        self.save_all_contacts(contacts)

    def remove_contact(self, contact_id):
        contacts = self.load_all_contacts()
        contacts = [contact for contact in contacts if contact["id"] != contact_id]
        self.save_all_contacts(contacts)

    def load_all_contacts(self):
        if not os.path.exists(CONTACTS_FILE):
            return []
        try:
            with open(CONTACTS_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return []

    def save_all_contacts(self, contacts):
        with open(CONTACTS_FILE, "w") as f:
            json.dump(contacts, f, indent=4)

if __name__ == "__main__":
    root = ctk.CTk()
    app = PhoneBookApp(root)
    root.mainloop()
