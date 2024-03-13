import re
import json
import datetime
import os
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
            raise ValueError("Invalid phone number format. Phone number should be 10 digits. Please try to use command change to User")

    def _validate_phone(self, value):
        return len(value) == 10 and value.isdigit()

class Birthday(Field):
    def __init__(self, value):
        self.value = datetime.datetime.strptime(value, '%d.%m.%Y')

    def __str__(self):
        return self.value.strftime('%d.%m.%Y')

class Notion(Field):
    def __init__(self, text):
        super().__init__(text)
        self.hashtags = self._find_hashtags()

    def _find_hashtags(self):
        return re.findall(r"#\w+", self.value)

    def edit_notion(self, new_text):
        self.value = new_text
        self.hashtags = self._find_hashtags()

class Record:
    def __init__(self, name):
        self.name = Name(*name.split())
        self.phones = []
        self.birthday = None
        self.notions = []

    def add_phone(self, phone):
        try:
            self.phones.append(Phone(phone))
        except ValueError as e:
            print(e)

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if str(p) != phone]

    def edit_phone(self, old_phone_index, new_phone):
        try:
            old_phone_index = int(old_phone_index)
            if 0 <= old_phone_index < len(self.phones):
                self.phones[old_phone_index] = Phone(new_phone)
                print("Номер телефону успішно змінено!")
            else:
                print("Невірний індекс номера телефону.")
        except ValueError:
            print("Невірний індекс номера телефону. Будь ласка, введіть коректний номер.")

    def display_phones(self):
        for i, phone in enumerate(self.phones):
            print(f"{i}: {phone}")

    def find_phone(self, phone):
        for p in self.phones:
            if str(p) == phone:
                return p
        return None

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def show_birthday(self):
        if self.birthday:
            return str(self.birthday)
        else:
            return "День народження не встановлено"

    def add_notion(self, notion):
        self.notions.append(Notion(notion))

    def edit_notion(self, notion_index, new_text):
        try:
            notion_index = int(notion_index)
            if 0 <= notion_index < len(self.notions):
                self.notions[notion_index].edit_notion(new_text)
                print("Нотатку успішно змінено!")
            else:
                print("Невірний індекс нотатки.")
        except ValueError:
            print("Невірний індекс нотатки. Будь ласка, введіть коректний номер.")

    def remove_notion(self, notion_index):
        try:
            notion_index = int(notion_index)
            if 0 <= notion_index < len(self.notions):
                del self.notions[notion_index]
                print("Нотатку успішно видалено!")
            else:
                print("Невірний індекс нотатки.")
        except ValueError:
            print("Невірний індекс нотатки. Будь ласка, введіть коректний номер.")

    def display_notions(self):
        for i, notion in enumerate(self.notions):
            print(f"{i}: {notion}")

    def __str__(self):
        notions_str = '; '.join([str(notion) for notion in self.notions])
        return f"Контакт: {self.name}, телефони: {'; '.join(str(p) for p in self.phones)}, день народження: {self.show_birthday()}, нотатки: {notions_str}"

class AddressBook(UserDict):
    def __init__(self, filename="contacts_book.json"):
        super().__init__()
        self.filename = filename
        self.load_from_json()

    def load_from_json(self):
        if os.path.exists(self.filename):
            try:
                with open(self.filename, "r") as file:
                    data = json.load(file)
                    for item in data:
                        record = Record(item["name"])
                        for phone in item.get("phones", []):
                            if phone is not None:
                                record.add_phone(phone)
                        birthday = item.get("birthday")
                        if birthday and birthday != 'None':
                            record.add_birthday(birthday)
                        for notion_item in item.get("notions", []):
                            record.add_notion(notion_item["text"])
                        self.add_record(record)
                print(f"Дані успішно завантажено з {self.filename}!")
            except (FileNotFoundError, json.JSONDecodeError) as e:
                print(f"Помилка при завантаженні з файлу {self.filename}: {e}")

    def save_to_json(self):
        with open(self.filename, 'w') as f:
            json.dump([{
                "name": record.name.value,
                "phones": [str(phone) for phone in record.phones],
                "birthday": str(record.birthday) if record.birthday else None,
                "notions": [{"text": notion.value, "hashtags": notion.hashtags} for notion in record.notions]
            } for record in self.data.values()], f, indent=4)
        print(f"Дані успішно збережено до {self.filename}!")

    def add_record(self, record):
        super().add_record(record)
        self.save_to_json()

