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
            raise ValueError("Неправильний формат номеру телефону. Номер повинен містити 10 цифр.")

    def _validate_phone(self, value):
        return len(value) == 10 and value.isdigit()

class Birthday(Field):
    def __init__(self, value):
        self.value = datetime.datetime.strptime(value, '%d.%m.%Y')
        try:
            self.value = datetime.datetime.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise ValueError("Неправильний формат дати народження. Використовуйте формат ДД.ММ.РРРР.")

    def __str__(self):
        return self.value.strftime('%d.%m.%Y')

    def __str__(self):
        return self.value.strftime('%d.%m.%Y')
class Notion:
    def __init__(self, text, hashtags):
        self.text = self._validate_text(text)
        self.hashtags = self._validate_hashtags(hashtags)

    def _validate_text(self, text):
        if not text or len(text) > 280:
            raise ValueError("Текст нотатки не може бути порожнім або перевищувати 280 символів.")
        return text

    def _validate_hashtags(self, hashtags):
        validated_hashtags = []
        pattern = re.compile(r"^#\w+$")
        for hashtag in hashtags.split():
            if pattern.match(hashtag):
                validated_hashtags.append(hashtag)
            else:
                raise ValueError("Неправильний формат хештегу.")
        return validated_hashtags

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
            old_phone_index = int(old_phone_index)  # Конвертуємо введений індекс в ціле число
            if 0 <= old_phone_index < len(self.phones):  # Перевіряємо, чи введений індекс знаходиться в межах списку телефонів
                self.phones[old_phone_index] = Phone(new_phone)  # Міняємо вибраний номер на новий
                print("Phone number changed successfully!")
            else:
                print("Невірний індекс номеру телефону.")
        except ValueError:
            print("Невірний індекс номеру телефону. Будь ласка, введіть коректний номер.")

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
        return f"Contact name: {self.name}, phones: {'; '.join(str(p) for p in self.phones)}, birthday: {self.show_birthday()}"
    
    def add_notion(self, text, hashtags):
        self.notions.append(Notion(text, hashtags))

    def edit_notion(self, index, new_text, new_hashtags):
        if 0 <= index < len(self.notions):
            self.notions[index] = Notion(new_text, new_hashtags)
            print("Нотатку успішно змінено.")
        else:
            raise ValueError("Неправильний індекс нотатки.")

    def delete_notion(self, index):
        if 0 <= index < len(self.notions):
            del self.notions[index]
            print("Нотатку успішно видалено.")
        else:
            raise ValueError("Неправильний індекс нотатки.")

class AddressBook(UserDict):
    def __init__(self):
        super().__init__()
        self.filename = "contacts_book.json"
        self.load_from_json()

    def find(self, name):
        # Перевіряємо ім'я контакту у нижному регістрі
        name_lower = name.lower()
        return self.data.get(name_lower)

@@ -99,184 +128,247 @@ def add_record(self, record):

    def delete(self, name):
        name_lower = name.lower()
        # Використовуємо ім'я контакту у нижному регістрі як ключ для видалення
        if name_lower in self.data:
            del self.data[name_lower]
            print(f"Контакт {name} успішно видалено!")
        else:
            print("Контакт не знайдено!")

    def add_record(self, record):
     self.data[record.name.value.lower()] = record

    def find_by_notion_or_hashtag(self, hashtag):
        results = []
        for name, record in self.data.items():
            for notion in record.notions:
                if hashtag in notion.hashtags:
                    results.append(name)
                    break
        return results

    def sort_by_hashtag(self, hashtag):
        sorted_records = []
        for name, record in self.data.items():
            for notion in record.notions:
                if hashtag in notion.hashtags:
                    sorted_records.append(name)
                    break
        return sorted(sorted_records)

    def birthdays(self):
        today = datetime.datetime.now()
        birthdays_this_week = {'Monday': [], 'Tuesday': [], 'Wednesday': [], 'Thursday': [], 'Friday': [], 'Saturday': [], 'Sunday': []}
        for record in self.data.values():
            if record.birthday:
                birthday_date = record.birthday.value
                next_birthday = birthday_date.replace(year=today.year)
                if next_birthday < today:
                    next_birthday = next_birthday.replace(year=today.year + 1)
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

        upcoming_birthdays = []        for day, names in birthdays_this_week.items():
            if names:
                print(f"{day}: {', '.join(names)}")
                upcoming_birthdays.extend(names)

        return upcoming_birthdays
    def load_from_json(self):
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
                self.data.clear()
                for record_data in data:
                    record = Record(record_data["name"])
                    for phone in record_data.get("phones", []):
                        record.add_phone(phone)
                    birthday = record_data.get("birthday")
                    if birthday:
                        record.add_birthday(birthday)
                    for notion_data in record_data.get("notions", []):
                        hashtags = ' '.join(notion_data["hashtags"])
                        record.add_notion(notion_data["text"], hashtags)
                    self.add_record(record)
        print("Дані успішно збережено.")

    def load_from_json(self):
        try:
            with open(self.filename, 'r') as f:
                data = json.load(f)
                self.data.clear()
                for record_data in data:
                    record = Record(record_data["name"])
                    for phone in record_data.get("phones", []):
                        record.add_phone(phone)
                    birthday = record_data.get("birthday")
                    if birthday:
                        record.add_birthday(birthday)
                    for notion_data in record_data.get("notions", []):
                        hashtags = ' '.join(notion_data["hashtags"])
                        record.add_notion(notion_data["text"], hashtags)
                    self.add_record(record)
            print("Дані успішно завантажено.")
        except FileNotFoundError:
            print("Файл не знайдено. Буде створено новий файл при збереженні.")
        except json.JSONDecodeError:
            print("Помилка при завантаженні даних. Файл може бути пошкоджений.")

def main():
    book = AddressBook()

    while True:
        command = input("\nДоступні команди:\n"
                        "hello -- для допомоги\n"
                        "add [ім'я] [телефон] -- для додавання контакту\n"
                        "change [ім'я] [телефон] -- для зміни номера телефону контакту\n"
                        "phone [ім'я] -- для отримання номера телефону контакту\n"
                        "delete [ім'я] -- для видалення контакту\n"
                        "all -- для перегляду всіх контактів\n"
                        "add-birthday [ім'я] [дата] -- для додавання дня народження контакту\n"
                        "show-birthday [ім'я] -- для перегляду дня народження контакту\n"
                        "add-notion [ім'я] [текст] [хештеги] -- для додавання нотатки до контакту\n"
                        "edit-notion [ім'я] [індекс] [новий текст] [нові хештеги] -- для редагування нотатки\n"
                        "delete-notion [ім'я] [індекс] -- для видалення нотатки\n"
                        "find-notions [хештег] -- для пошуку нотаток за хештегами\n"
                        "sort-by-hashtag [хештег] -- для сортування контактів за хештегом\n"
                        "save -- для збереження даних у файл\n"
                        "load -- для завантаження даних з файлу\n"
                        "q -- для виходу\n"
                        "\nВведіть команду:").strip().lower()

        if command in ['q', 'good bye', 'close', 'exit', 'quit']:
            break
        elif command == 'add':
            name = input("Введіть ім'я контакту: ").strip()
            phone = input("Введіть номер телефону: ").strip()
            record = Record(name)
            record.add_phone(phone)
            book.add_record(record)
            print(f"Контакт {name} додано успішно!")
        elif command == 'change':
            name = input("Введіть ім'я контакту: ").strip().lower()
            if name in book.data:
                contact = book.data[name]
                if not contact.phones:
                    phone = input("Введіть новий номер телефону: ").strip()
                    contact.add_phone(phone)
                else:
                    contact.display_phones()
                    old_phone_index = input("Введіть індекс номера телефону, який хочете змінити: ")
                    new_phone = input("Введіть новий номер телефону: ").strip()
                    contact.edit_phone(old_phone_index, new_phone)
            else:
                print("Контакт не знайдено.")

        elif command == 'phone':
            name = input("Введіть ім'я контакту: ").strip().lower()
            if name in book.data:
                contact = book.data[name]
                contact.display_phones()
            else:
                print("Контакт не знайдено.")

        elif command == 'delete':
            name = input("Введіть ім'я контакту для видалення: ").strip().lower()
            book.delete(name)

        elif command == 'all':
            if book.data:
                for name, record in book.data.items():
                    print(record)
            else:
                print("Адресна книга порожня.")

        elif command == 'add-birthday':
            name = input("Введіть ім'я контакту: ").strip().lower()
            birthday = input("Введіть дату народження (ДД.ММ.РРРР): ").strip()
            if name in book.data:
                book.data[name].add_birthday(birthday)
                print(f"День народження для {name} успішно додано.")
            else:
                print("Контакт не знайдено.")

        elif command == 'show-birthday':
                name = input("Введіть ім'я контакту: ").strip().lower()
                if name in book.data and book.data[name].birthday:
                    print(f"День народження {name}: {book.data[name].show_birthday()}")
                else:
                    print("Контакт або день народження не знайдено.")

        elif command.startswith("add-notion"):
            parts = command.split(" ", 3)
            if len(parts) < 4:
                print("Недостатньо даних для додавання нотатки. Потрібно ім'я, текст і хештеги.")
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
                name = parts[1]
                text = parts[2]
                hashtags = parts[3]
                if name in book.data:
                    try:
                        book.data[name].add_notion(text, hashtags)
                        print(f"До контакту {name} додано нотатку.")
                    except ValueError as e:
                        print(e)
                else:
                    print("Контакт не знайдено.")

        elif command.startswith("edit-notion"):
            parts = command.split(" ", 4)
            if len(parts) < 5:
                print("Недостатньо даних для редагування нотатки. Потрібно ім'я, індекс, новий текст і нові хештеги.")
            else:
                name = parts[1]
                index = parts[2]
                new_text = parts[3]
                new_hashtags = parts[4]
                if name in book.data:
                    try:
                        book.data[name].edit_notion(index, new_text, new_hashtags)
                        print("Нотатку успішно змінено.")
                    except ValueError as e:
                        print(e)
                else:
                    print("Контакт не знайдено.")

        elif command.startswith("delete-notion"):
            parts = command.split(" ", 3)
            if len(parts) < 3:
                print("Недостатньо даних для видалення нотатки. Потрібно ім'я і індекс нотатки.")
            else:
                name = parts[1]
                index = parts[2]
                if name in book.data:
                    try:
                        book.data[name].delete_notion(index)
                        print("Нотатку успішно видалено.")
                    except ValueError as e:
                        print(e)
                else:
                    print("Контакт не знайдено.")

        elif command.startswith("find-notions"):
            hashtag = command.split(" ", 1)[1]
            results = book.find_by_notion_or_hashtag(hashtag)
            if results:
                print("Знайдені контакти з нотатками, що містять хештег:", hashtag)
                for result in results:
                    print(result)
            else:
                print("Нотатки з таким хештегом не знайдено.")

        elif command.startswith("sort-by-hashtag"):
            hashtag = command.split(" ", 1)[1]
            sorted_contacts = book.sort_by_hashtag(hashtag)
            if sorted_contacts:
                print("Контакти, відсортовані за наявністю хештегу:", hashtag)
                for contact_name in sorted_contacts:
                    print(contact_name)
            else:
                print("Контакти з таким хештегом не знайдено.")

        elif command == "save":
            book.save_to_json()
            print("Дані успішно збережено.")

        elif command == "load":
            book.load_from_json()
            print("Дані успішно завантажено.")

        elif command == "hello":
            print("Привіт! Як я можу допомогти вам сьогодні?")

        elif command == "birthdays":
            pass

        else:
            print("Невідома команда. Будь ласка, спробуйте ще раз.")

if __name__ == "__main__":
    main()