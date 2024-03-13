import json
import datetime
import re
from collections import UserDict, namedtuple

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)

class Name(Field):
    def __init__(self, first_name, last_name=None):
        full_name = f"{first_name} {last_name}" if last_name else first_name
        super().__init__(full_name)

class Phone(Field):
    def __init__(self, value):
        if self._validate_phone(value):
            super().__init__(value)
        else:
            raise ValueError("Неправильний формат номеру телефону. Повинен бути 10 цифр.")

    def _validate_phone(self, value):
        return len(value) == 10 and value.isdigit()

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.datetime.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise ValueError("Неправильний формат дати. Використовуйте формат ДД.ММ.РРРР.")

    def __str__(self):
        return self.value.strftime('%d.%m.%Y')

class Email(Field):
    def __init__(self, value):
        if self._validate_email(value):
            super().__init__(value)
        else:
            raise ValueError("Неправильний формат електронної адреси.")

    def _validate_email(self, value):
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return re.match(pattern, value) is not None

AddressComponents = namedtuple('AddressComponents', ['вулиця', 'номер_будинку', 'місто', 'поштовий_індекс', 'країна'])

class Address(Field):
    def __init__(self, street, house_number, city, postal_code, country):
        address_components = AddressComponents(street, house_number, city, postal_code, country)
        if self._validate_address(address_components):
            super().__init__(address_components)
        else:
            raise ValueError("Неправильні компоненти адреси.")

    def _validate_address(self, components):
        return all(components) and all(type(component) == str for component in components)

    def __str__(self):
        return f"{self.value.вулиця}, {self.value.номер_будинку}, {self.value.місто}, {self.value.поштовий_індекс}, {self.value.країна}"

class Notions:
    def __init__(self):
        self.notes = {}
        self.hashtags = {}

    def add_note(self, note, tags=None):
        note_id = len(self.notes) + 1
        self.notes[note_id] = note
        if tags:
            self.hashtags[note_id] = tags.split()

    def edit_note(self, note_id, new_note, tags=None):
        if note_id in self.notes:
            self.notes[note_id] = new_note
            if tags:
                self.hashtags[note_id] = tags.split()

    def delete_note(self, note_id):
        if note_id in self.notes:
            del self.notes[note_id]
            if note_id in self.hashtags:
                del self.hashtags[note_id]

    def find_by_tag(self, tag):
        results = []
        for note_id, tags in self.hashtags.items():
            if tag in tags:
                results.append(self.notes[note_id])
        return results

class Record:
    def __init__(self, name):
        self.name = Name(*name.split())
        self.phones = []
        self.birthday = None
        self.email = None
        self.address = None
        self.notions = Notions()

class AddressBook(UserDict):
    def find_contacts_by_note_or_tag(self, search_query):
        matching_contacts = []
        for name, record in self.data.items():
            if any(search_query in note for note in record.notions.notes.values()):
                matching_contacts.append(name)
            elif any(search_query in tag for tags in record.notions.hashtags.values() for tag in tags):
                matching_contacts.append(name)
        return matching_contacts

    def get_contacts_by_tag(self, tag):
        tagged_contacts = {}
        for name, record in self.data.items():
            if tag in record.notions.hashtags.values():
                tagged_contacts[name] = record
        return tagged_contacts

    def display_contacts_by_tag(self, tag):
        tagged_contacts = self.get_contacts_by_tag(tag)
        for name in tagged_contacts:
            print(name)

    def save_to_json(self, filename='contacts_book.json'):
        data_to_save = []
        for name, record in self.data.items():
            data_to_save.append({
                "name": record.name.value,
                "phones": [str(phone) for phone in record.phones],
                "birthday": str(record.birthday) if record.birthday else "",
                "email": str(record.email) if record.email else "",
                "address": str(record.address) if record.address else "",
                "notes": [{"note": note, "tags": ' '.join(tags)} for note_id, (note, tags) in enumerate(zip(record.notions.notes.values(), record.notions.hashtags.values()))]
            })
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data_to_save, f, ensure_ascii=False, indent=4)

    def load_from_json(self, filename='contacts_book.json'):
        try:
            with open(filename, "r", encoding='utf-8') as f:
                records_json = json.load(f)
                for record_json in records_json:
                    record = Record(record_json["name"])
                    for phone in record_json.get("phones", []):
                        record.phones.append(Phone(phone))
                    if record_json.get("birthday"):
                        record.birthday = Birthday(record_json["birthday"])
                    if record_json.get("email"):
                        record.email = Email(record_json["email"])
                    if record_json.get("address"):
                        address_components = record_json["address"].split(", ")
                        if len(address_components) == 5:
                            record.address = Address(*address_components)
                    for note_info in record_json.get("notes", []):
                        record.notions.add_note(note_info["note"], note_info.get("tags", ""))
                    self.data[record.name.value] = record
        except FileNotFoundError:
            print(f"Файл {filename} не знайдено.")
        except json.JSONDecodeError:
            print(f"Помилка при декодуванні JSON з файлу {filename}.")
