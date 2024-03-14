import json
import datetime
import re
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
            raise ValueError("\n Невірний формат номеру телефону. Номер телефону має складатися з 10 цифр.")

    def _validate_phone(self, value):
        return len(value) == 10 and value.isdigit()

class Birthday(Field):
    def __init__(self, value):
        self.value = datetime.datetime.strptime(value, '%d.%m.%Y')

    def __str__(self):
        return self.value.strftime('%d.%m.%Y')

class Notion:
    def __init__(self, text, hashtags):
        self.text = self.validate_text(text)
        self.hashtags = self.validate_hashtags(hashtags)

    @staticmethod
    def validate_text(text, max_length=280):
        if not text or len(text) > max_length:
            raise ValueError("Текст нотатки пустий або перевищує максимальну допустиму довжину.")
        return text

    @staticmethod
    def validate_hashtags(hashtags):
        pattern = re.compile(r"^#[\w]+$")
        validated_hashtags = []
        for hashtag in hashtags:
            if not pattern.match(hashtag):
                raise ValueError("Невірний формат хештегу. Хештеги повинні починатися з символу #.")
            validated_hashtags.append(hashtag)
        return validated_hashtags

class Record:
    def __init__(self, name):
        self.name = Name(*name.split())
        self.phones = []
        self.birthday = None
        self.notions = []

    def add_phone(self, phone):
        self.phones.append(Phone(phone))

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if str(p) != phone]

    def edit_phone(self, old_phone_index, new_phone):
        old_phone_index = int(old_phone_index)
        if 0 <= old_phone_index < len(self.phones):
            self.phones[old_phone_index] = Phone(new_phone)
            print("Номер телефону успішно змінено!")
        else:
            print("Невірний індекс номеру телефону.")

    def add_notion(self, text, hashtags):
        self.notions.append(Notion(text, hashtags))

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def show_birthday(self):
        if self.birthday:
            return str(self.birthday)
        else:
            return "Дата народження не встановлена"

    def __str__(self):
        return f"Ім'я контакту: {self.name}, телефони: {'; '.join(str(p) for p in self.phones)}, дата народження: {self.show_birthday()}"

class AddressBook(UserDict):
    def __init__(self):
        super().__init__()
        self.load_from_json()

    def add_record(self, record):
        self.data[record.name.value.lower()] = record

    def save_to_json(self, filename="contacts_book.json"):
        with open(filename, 'w') as f:
            json.dump([{
                "name": record.name.value,
                "phones": [str(phone) for phone in record.phones],
                "birthday": str(record.birthday) if record.birthday else None,
                "notions": [{"text": notion.text, "hashtags": notion.hashtags} for notion in record.notions]
            } for record in self.data.values()], f, indent=4)

    def load_from_json(self, filename="contacts_book.json"):
        try:
            with open(filename, "r") as file:
                data = json.load(file)
                for item in data:
                    record = Record(item["name"])
                    for phone in item.get("phones", []):
                        record.add_phone(phone)
                    birthday = item.get("birthday")
                    if birthday and birthday != 'None':
                        record.add_birthday(birthday)
                    for notion in item.get("notions", []):
                        record.add_notion(notion["text"], notion.get("hashtags", []))
                    self.add_record(record)
            print("Дані успішно завантажено.")
        except FileNotFoundError:
            print("Файл не знайдено.")
        except json.JSONDecodeError:
            print("Помилка декодування JSON.")

def main():
    # Create an instance of AddressBook
    address_book = AddressBook()

    # Perform desired operations on the address book
    # For example, add a record
    record = Record("John Doe")
    record.add_phone("1234567890")
    address_book.add_record(record)

    # Save the address book to JSON
    address_book.save_to_json()

    # Load the address book from JSON
    address_book.load_from_json()

if __name__ == "__main__":
    main()
