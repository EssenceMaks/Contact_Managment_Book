import re
import json
import datetime
from collections import UserDict


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, first_name, last_name=None):
        if last_name:
            super().__init__(f"{first_name} {last_name}")
        else:
            super().__init__(first_name)


class Phone(Field):
    def __init__(self, value):
        if self._validate_phone(value):
            super().__init__(value)
        else:
            raise ValueError("\n Invalid phone number format. \n Phone number should be 10 digits. \n PLease try to use comand change to User")

    def _validate_phone(self, value):
        return len(value) == 10 and value.isdigit()


class Birthday(Field):
    def __init__(self, value):
        self.value = datetime.datetime.strptime(value, '%d.%m.%Y')

    def __str__(self):
        return self.value.strftime('%d.%m.%Y')

class Email(Field):
    def __init__(self, value):
        # Зберігаємо pattern для повторного використання
        self.pattern = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
        # Зберігаємо email, якщо він валідний
        self.value = value
        if not self.pattern.match(value):
            # Викидаємо помилку для невалідного email
            raise ValueError("Invalid email address")

class Find:
    @staticmethod
    def find_by_name(address_book, name):
        found_contacts = []
        for record in address_book.values():
            if record.name.value.lower() == name.lower():
                found_contacts.append(record)
        return found_contacts

    @staticmethod
    def find_by_phone(address_book, phone):
        found_contacts = []
        for record in address_book.values():
            for record_phone in record.phones:
                if str(record_phone) == phone:
                    found_contacts.append(record)
                    break
        return found_contacts
    
    @staticmethod
    def find_by_birthday(address_book, birthday):
        found_contacts = []
        for record in address_book.values():
            if record.birthday and str(record.birthday) == birthday:
                found_contacts.append(record)
        return found_contacts


class Record:
    def __init__(self, name):
        self.name = Name(*name.split())
        self.phones = []
        self.email = None
        self.birthday = None

    def add_phone(self, phone):
        try:
            self.phones.append(Phone(phone))
        except ValueError as e:
            print(e)

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if str(p) != phone]

    def edit_phone(self, old_phone_index, new_phone):
        try:
            # Конвертуємо введений індекс в ціле число
            old_phone_index = int(old_phone_index)
            # Перевіряємо, чи введений індекс знаходиться в межах списку телефонів
            if 0 <= old_phone_index < len(self.phones):
                # Міняємо вибраний номер на новий
                self.phones[old_phone_index] = Phone(new_phone)
                print("Phone number changed successfully!")
            else:
                print("Invalid phone number index.")
        except ValueError:
            print("Invalid phone number index. Please enter a valid number.")

    def display_phones(self):
        for i, phone in enumerate(self.phones):
            print(f"{i}: {phone}")

    def find_phone(self, phone):
        for p in self.phones:
            if str(p) == phone:
                return p
        return None
    
    def add_email(self, email):
        self.email = Email(email)

    def show_email(self):
        if self.email:
            return str(self.email)
        else:
            return "No email added"

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def show_birthday(self):
        if self.birthday:
            return str(self.birthday)
        else:
            return "Birthday not set"

    def __str__(self):
        return f"Contact name: {self.name}, phones: {'; '.join(str(p) for p in self.phones)}, email: {self.email}, birthday: {self.show_birthday()}"


class AddressBook(UserDict):

    def find(self, name):
        # Перевіряємо ім'я контакту у нижному регістрі
        name_lower = name.lower()
        return self.data.get(name_lower)

    def add_record(self, record):
        self.data[record.name.value.lower()] = record

    def delete(self, name):
        name_lower = name.lower()
        # Використовуємо ім'я контакту у нижному регістрі як ключ для видалення
        if name_lower in self.data:
            del self.data[name_lower]
            print(f"Contact {name} deleted successfully!")
        else:
            print("Contact not found!")

    def birthdays(self):
        today = datetime.datetime.now()
        birthdays_this_week = {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': [], 'Saturday': [], 'Sunday': []}

        for record in self.data.values():
            if record.birthday:
                birthday_date = record.birthday.value
                next_birthday = birthday_date.replace(year=today.year)
                if next_birthday < today:
                    next_birthday = birthday_date.replace(year=today.year + 1)
                delta_days = (next_birthday - today).days
                birthday_weekday = next_birthday.strftime('%A')

                if 0 <= delta_days < 7:
                    if birthday_weekday in ['Saturday', 'Sunday']:
                        if 'Next Monday' not in birthdays_this_week:
                            birthdays_this_week['Next Monday'] = []
                        birthdays_this_week['Next Monday'].append(f"{record.name.value} (from {birthday_weekday})")
                    else:
                        birthdays_this_week[birthday_weekday].append(record.name.value)
                elif delta_days == 7:
                    if 'Next Monday' not in birthdays_this_week:
                        birthdays_this_week['Next Monday'] = []
                    birthdays_this_week['Next Monday'].append(f"{record.name.value} (will be on {birthday_weekday})")

        upcoming_birthdays = []
        for day, names in birthdays_this_week.items():
            if names:
                print(f"{day}: {', '.join(names)}")
                upcoming_birthdays.extend(names)

        return upcoming_birthdays

    def save_to_json(self, filename):
        with open(filename, 'w') as f:
            json.dump([{
                "name": record.name.value,
                "phones": [str(phone) for phone in record.phones],
                "email": str(record.email),
                "birthday": str(record.birthday)
            } for record in self.data.values()], f, indent=4)

    def load_from_json(self, filename):
        try:
            with open(filename, "r") as file:
                data = json.load(file)
                for item in data:
                    record = Record(item["name"])
                    for phone in item.get("phones", []):
                        if phone is not None:
                            record.add_phone(phone)
                    email = item.get("email")
                    if email is not None:
                        if email != 'None':
                            record.add_email(email)
                    birthday = item.get("birthday")
                    if birthday is not None:
                        if birthday != 'None':
                            record.add_birthday(birthday)
                    self.add_record(record)
            print(f"Data loaded from {filename} successfully!")
        except FileNotFoundError:
            print(f"File '{filename}' not found.")
        except json.JSONDecodeError:
            print(f"Error decoding JSON from file '{filename}'.")


def main():
    book = AddressBook()

    while True:
        command = input("\nAvailable commands:\n"
                        "\n"
                        "hello                         -- to get assistance\n"
                        "add [ім'я] [телефон]          -- to add a contact\n"
                        "change [ім'я] [телефон]       -- to change a contact's phone number\n"
                        "phone [ім'я]                  -- to get a contact's phone number\n"
                        "delete [ім'я]                 -- to delete a contact\n"
                        "all                           -- to show all contacts\n"
                        "add-email [ім'я] [email]      -- to add an email for a contact\n"
                        "show-email [ім'я]             -- to show a contact's email\n"
                        "add-birthday [ім'я] [дата]    -- to add a birthday for a contact\n"
                        "show-birthday [ім'я]          -- to show a contact's birthday\n"
                        "birthdays                     -- to show upcoming birthdays\n"
                        "find-name [ім'я]              -- to find a contact by name\n"
                        "find-phone [телефон]          -- to find a contact by phone\n"
                        "find-birth [дата]             -- to find a contact by birthday\n"
                        "save [файл.json]              -- to save contacts to a JSON file\n"
                        "load [файл.json]              -- to load contacts from a JSON file\n"
                        "q /good bye/close/exit/quit   -- to exit the assistant\n"
                        "\n"
                        "Enter a command:").strip().lower()

        if command in ['q', 'good bye', 'close', 'exit', 'quit']:
            break
        elif command == 'add':
            name = input("Enter contact name: ").strip()
            phone = input("Enter phone number: ").strip()
            record = Record(name)
            record.add_phone(phone)
            book.add_record(record)
            print(f"Contact {name} added successfully!")
            
        elif command == 'change':
            name = input("Enter contact name: ").strip().lower()
            if name in book.data:
                contact = book.data[name]
                if not contact.phones:
                    phone = input("Enter phone number: ").strip()
                    contact.add_phone(phone)
                else:
                    contact.display_phones()
                    old_phone_index = input("Enter the index of the phone number you want to change: ")
                    new_phone = input("Enter new phone number: ").strip()
                    contact.edit_phone(old_phone_index, new_phone)
            else:
                print("Contact not found!")

        elif command == 'phone':
            name = input("Enter contact name: ").strip().lower()
            if name in book.data:
                print(f"Phone number(s) for {book.data[name].name.value}: {', '.join([str(phone) for phone in book.data[name].phones])}")
            else:
                print("Contact not found!")

        elif command == 'delete':
            name = input("Enter contact name: ").strip().lower()
            if name in book.data:
                del_contact_name = book.data[name].name.value
                book.delete(name)
                print(f"Contact {del_contact_name} deleted successfully!")
            else:
                print("Contact not found!")

        elif command == 'all':
            for record in book.data.values():
                print(record)

        elif command == 'add-email':
            name = input("Enter contact name: ").strip().lower()
            email = input("Enter email: ").strip()
            if name in book.data:
                book.data[name].add_email(email)
                print(f"Email added successfully for contact {book.data[name].name.value}!")
            else:
                print("Contact not found!")

        elif command == 'show-email':
            name = input("Enter contact name: ").strip().lower()
            if name in book.data:
                print(f"Email for {book.data[name].name.value}: {book.data[name].show_email()}")
            else:
                print("Contact not found!")

        elif command == 'add-birthday':
            name = input("Enter contact name: ").strip().lower()
            birthday = input("Enter birthday (DD.MM.YYYY): ").strip()
            if name in book.data:
                book.data[name].add_birthday(birthday)
                print(f"Birthday added successfully for contact {book.data[name].name.value}!")
            else:
                print("Contact not found!")

        elif command == 'show-birthday':
            name = input("Enter contact name: ").strip().lower()
            if name in book.data:
                print(f"Birthday for {book.data[name].name.value}: {book.data[name].show_birthday()}")
            else:
                print("Contact not found!")

        elif command == 'birthdays':
            upcoming_birthdays = book.birthdays()
            print("\nUpcoming birthdays:")
            for name in upcoming_birthdays:
                contact = book.find(name)
                if contact:
                    phone_number = ", ".join(str(phone) for phone in contact.phones) if contact.phones else "No phone number"
                    print(f"{name}'s birthday is on {contact.birthday} number for call {phone_number}")
                else:
                    print(f"No contact found for {name}")

        elif command == 'find-name':
            name_to_find = input("Enter name to find: ")
            found_contacts = Find.find_by_name(book, name_to_find)
            if found_contacts:
                print("Found contacts:")
                for contact in found_contacts:
                    print(contact)
            else:
                print("No contacts found.")

        elif command == 'find-phone':
            phone_to_find = input("Enter phone number to find: ")
            found_contacts = Find.find_by_phone(book, phone_to_find)
            if found_contacts:
                print("Found contacts:")
                for contact in found_contacts:
                    print(contact)
            else:
                print("No contacts found.")

        elif command == 'find-birth':
            birthday_to_find = input("Enter birthday to find (dd.mm.yyyy): ")
            found_contacts = Find.find_by_birthday(book, birthday_to_find)
            if found_contacts:
                print("Found contacts:")
                for contact in found_contacts:
                    print(contact)
            else:
                print("No contacts found.")

        elif command == 'save':
            filename = input("Enter the filename to save to (e.g., contacts.json): ").strip()
            book.save_to_json(filename)
            print("Contacts saved successfully!")

        elif command == 'load':
            filename = input("Enter the filename to load from (e.g., contacts.json): ").strip()
            book.load_from_json(filename)
            print("Contacts loaded successfully!")

        elif command == 'hello':
            print("Hello! How can I assist you?")

        else:
            print("\n Incorrect command. \nPlease try correct command.")


if __name__ == "__main__":
    main()