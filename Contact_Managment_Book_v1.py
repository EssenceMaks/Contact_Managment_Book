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
            raise ValueError("\n Неправильний формат номеру телефону. \n Номер телефону має складатися з 10 цифр. \n Будь ласка, спробуйте команду зміни для користувача")

    def _validate_phone(self, value):
        return len(value) == 10 and value.isdigit()


class Birthday(Field):
    def __init__(self, value):
        self.value = datetime.datetime.strptime(value, '%d.%m.%Y')

    def __str__(self):
        return self.value.strftime('%d.%m.%Y')


class Notions:
    def __init__(self):
        self.notes = {}
        self.hashtags = {}

    def add_note(self, note, tags=None):
        note_id = len(self.notes) + 1
        self.notes[note_id] = note
        if tags:
            self.hashtags[note_id] = tags.split()
        print("Нотатку успішно додано.")

    def edit_note(self, note_id, new_note, tags=None):
        if note_id in self.notes:
            self.notes[note_id] = new_note
            if tags:
                self.hashtags[note_id] = tags.split()
            print("Нотатку успішно оновлено.")
        else:
            print("Нотатку не знайдено.")

    def delete_note(self, note_id):
        if note_id in self.notes:
            del self.notes[note_id]
            if note_id in self.hashtags:
                del self.hashtags[note_id]
            print("Нотатку успішно видалено.")
        else:
            print("Нотатку не знайдено.")

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
        self.notions = Notions()

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
                print("Неправильний індекс номеру телефону.")
        except ValueError:
            print("Неправильний індекс номеру телефону. Будь ласка, введіть коректний номер.")

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

    def __str__(self):
        return f"Ім'я контакту: {self.name}, телефони: {'; '.join(str(p) for p in self.phones)}, день народження: {self.show_birthday()}"


class AddressBook(UserDict):

    def find(self, name):
        name_lower = name.lower()
        return self.data.get(name_lower)

    def add_record(self, record):
        self.data[record.name.value.lower()] = record

    def delete(self, name):
        name_lower = name.lower()
        if name_lower in self.data:
            del self.data[name_lower]
            print(f"Контакт {name} успішно видалено!")
        else:
            print("Контакт не знайдено!")

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
                        birthdays_this_week['Next Monday'].append(f"{record.name.value} (з {birthday_weekday})")
                    else:
                        birthdays_this_week[birthday_weekday].append(record.name.value)
                elif delta_days == 7:
                    if 'Next Monday' not in birthdays_this_week:
                        birthdays_this_week['Next Monday'] = []
                    birthdays_this_week['Next Monday'].append(f"{record.name.value} (буде в {birthday_weekday})")

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
                "birthday": str(record.birthday),
                "notes": [{"note": note, "tags": tags} for note_id, (note, tags) in enumerate(zip(record.notions.notes.values(), record.notions.hashtags.values()))]
            } for record in self.data.values()], f, indent=4)

    def load_from_json(self, filename):
        try:
            with open(filename, "r") as
