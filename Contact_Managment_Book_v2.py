import json
import datetime
import re
from collections import UserDict

class Address:
    def __init__(self, address):
        if len(address) <= 120:
            self.addresses = [address]
        else:
            raise ValueError("Address exceeds the maximum allowed length of 120 symbols.")

    def add_address(self, address):
        if isinstance(address, str):
            self.addresses.append(address)
        else:
            print("Invalid address format. Please provide a string.")

    def show_address(self, name):
        if self.addresses:
            return f"{name}'s address is {self.addresses[0]}"
        else:
            return "No address was provided"
            
    def edit_address(self, new_address):
        self.addresses = [new_address]
        return "Address has been successfully edited"

    def delete_address(self, address):
        self.addresses = [a for a in self.addresses if str(a) != str(address)]

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

    def _validate_phone(self,value):
        return len(value) == 10 and value.isdigit()

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.datetime.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise ValueError("Неправильний формат дати народження. Використовуйте формат ДД.ММ.РРРР.")

    def __str__(self):
        return self.value.strftime('%d.%m.%Y')

class Find:
    def find_by_name(address_book, name):
        found_contacts = []
        for record in address_book.values():
            if record.name.value.lower() == name.lower():
                found_contacts.append(record)
        return found_contacts  

    def find_by_phone(address_book, phone):
        found_contacts = []
        for record in address_book.values():
            for record_phone in record.phones:
                if str(record_phone) == phone:
                    found_contacts.append(record)
                    break
        return found_contacts
    
    def find_by_birthday(address_book, birthday):
        found_contacts = []
        for record in address_book.values():
            if record.birthday and str(record.birthday) == birthday:
                found_contacts.append(record)
        return found_contacts

class Notion:
    def __init__(self, text, hashtags):
        self.text = self._validate_text(text)
        self.hashtags = self._validate_hashtags(hashtags)

    def _validate_text(text):
        if not text or len(text) > 280:
            raise ValueError("Текст нотатки не може бути порожнім або перевищувати 280 символів.")
        return text

    def _validate_hashtags(hashtags):
        validated_hashtags = []
        pattern = re.compile(r"^#\w+$")
        for hashtag in hashtags.split():
            if pattern.match(hashtag):
                validated_hashtags.append(hashtag)
            else:
                raise ValueError("Неправильний формат хештегу.")
        return validated_hashtags

class Find:
    def find_by_name(address_book, name):
        found_contacts = []
        for record in address_book.values():
            if record.name.value.lower() == name.lower():
                found_contacts.append(record)
        return found_contacts
    
    def find_by_phone(address_book, phone):
        found_contacts = []
        for record in address_book.values():
            for record_phone in record.phones:
                if str(record_phone) == phone:
                    found_contacts.append(record)
                    break
        return found_contacts
    
    def find_by_birthday(address_book, birthday):
        found_contacts = []
        for record in address_book.values():
            if record.birthday and str(record.birthday) == birthday:
                found_contacts.append(record)
        return found_contacts


class Record:
    def __init__(self, name):
        self.original_name = name
        self.name = Name(*name.split())
        self.phones = []
        self.birthday = None
        self.notions = []
        self.address = None

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
                print("Номер телефону успішно змінено.")
            else:
                print("Невірний індекс номеру телефону.")
        except ValueError:
            print("Невірний індекс номеру телефону. Будь ласка, введіть коректний номер.")

    def add_record(self, record):
        self.data[record.name.value.lower()] = record

    def delete(self, name):
        pass

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
    
    def add_notion(self, text, hashtags):
        self.notions.append(Notion(text, hashtags))

    def edit_notion(self, index, new_text, new_hashtags):
        try:
            index = int(index)
            if 0 <= index < len(self.notions):
                self.notions[index] = Notion(new_text, new_hashtags)
                print("Нотатку успішно змінено.")
            else:
                print("Неправильний індекс нотатки.")
        except ValueError as e:
            print(e)

    def delete_notion(self, index):
        try:
            index = int(index)
            if 0 <= index < len(self.notions):
                del self.notions[index]
                print("Нотатку успішно видалено.")
            else:
                print("Неправильний індекс нотатки.")
        except ValueError as e:
            print(e)

    def __str__(self):
        phones_str = '; '.join([str(phone) for phone in self.phones])
        birthday_str = self.show_birthday() if self.birthday else "День народження не встановлено"
        notions_str = '; '.join([f"{notion.text} (Хештеги: {' '.join(notion.hashtags)})" for notion in self.notions])
        address_str = ', '.join(self.address.addresses) if hasattr(self, 'address') and self.address else "Адреса не встановлена"
        return f"Ім'я контакту: {self.original_name}, Телефони: {phones_str}, День народження: {birthday_str}, Нотатки: {notions_str}, Адреса: {address_str}"

    def add_hashtag_to_notion(self, notion_index, hashtag):
        try:
            notion_index = int(notion_index)
            if 0 <= notion_index < len(self.notions):
                if f"#{hashtag}" not in self.notions[notion_index].hashtags:
                    self.notions[notion_index].hashtags.append(f"#{hashtag}")
                    print(f"Хештег #{hashtag} успішно додано до нотатки.")
                else:
                    print(f"Хештег #{hashtag} вже існує в цій нотатці.")
            else:
                print("Невірний індекс нотатки.")
        except ValueError as e:
            print("Помилка при додаванні хештегу:", e)

    def remove_hashtag_from_notion(self, notion_index, hashtag):
        try:
            notion_index = int(notion_index)
            if 0 <= notion_index < len(self.notions):
                if f"#{hashtag}" in self.notions[notion_index].hashtags:
                    self.notions[notion_index].hashtags.remove(f"#{hashtag}")
                    print(f"Хештег #{hashtag} успішно видалено з нотатки.")
                else:
                    print(f"Хештег #{hashtag} не знайдено в цій нотатці.")
            else:
                print("Невірний індекс нотатки.")
        except ValueError as e:
            print("Помилка при видаленні хештегу:", e)

    def add_address(self, address):
        self.address = Address(address)

    def edit_address(self, new_address):
        self.address.edit_address(new_address)

    def delete_address(self, address):
        self.address = None
    
    def show_address(self):
        if self.address:
            return self.address.show_address(self.name.value)
        else:
            return "No address found"

class AddressBook(UserDict):
    def __init__(self):
        super().__init__()
        self.filename = "contacts_book.json"
        self.load_from_json()

    def add_record(self, record):
        key = record.name.value.lower()
        self.data[key] = record

    def find(self, name):
        name_lower = name.lower()
        return self.data.get(name_lower)

    def delete(self, name):
        name_lower = name.lower()
        if name_lower in self.data:
            del self.data[name_lower]
            print(f"Контакт {name} видалено успішно.")
        else:
            print("Контакт не знайдено.")

    def find_by_notion_or_hashtag(self, hashtag):
        found_records = []
        for record in self.data.values():
            for notion in record.notions:
                if hashtag in notion.hashtags:
                    found_records.append(record)
                    break  # Зупиняємо пошук, якщо знайдено хештег
        return found_records

    def sort_by_hashtag(self, hashtag):
        sorted_records = []
        for record in self.data.values():
            for notion in record.notions:
                if hashtag in notion.hashtags:
                    sorted_records.append(record.name.value)
                    break  # Зупиняємо, якщо знайдено хештег
        return sorted(sorted_records, key=lambda x: x.lower())

    def all_names(self):
            formatted_names = []
            for name in self.data.keys():
                formatted_name = ' '.join([part.capitalize() for part in name.split()])
                formatted_names.append(formatted_name)
            return formatted_names

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
    
    def edit_address(self, name, new_address):
        name_key = name.lower()
        if name_key in self.data:
            record = self.data[name_key]
            if record.address:
                record.address.edit_address(new_address)
                print(f"Address for {name} has been successfully edited to {new_address}.")
            else:
                print(f"No address has been added to {name} yet.")
        else:
            print(f"Contact {name} not found.")
#_______________________________________________________________________________________________________________________________
    def save_to_json(self, filename="contacts_book.json"):
        with open(filename, 'w') as f:
            json_data = []
            for record in self.data.values():
                record_data = {
                    'name': str(record.name),
                    'phones': [str(phone) for phone in record.phones],
                    'birthday': str(record.birthday) if record.birthday else None,
                    'notions': [{'text': notion.text, 'hashtags': notion.hashtags} for notion in record.notions],
                    "addresses": record.address.addresses if record.address else []
                }
                json_data.append(record_data)
            json.dump(json_data, f, ensure_ascii=False, indent=4)
        return "Дані успішно збережено у файлі " + filename + "."

    def load_from_json(self, filename="contacts_book.json"):
        try:
            with open(filename, 'r') as f:
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
                    addresses = record_data.get("addresses", [])
                    if addresses:
                        for address in addresses:
                            record.add_address(address)
                    self.add_record(record)
            print("Дані успішно завантажено з файлу " + filename + ".")
        except FileNotFoundError:
            print("Файл не знайдено. Буде створено новий файл при збереженні.")
        except json.JSONDecodeError:
            print("Помилка при завантаженні даних. Файл може бути пошкоджений.")
#_______________________________________________________________________________________________________________________________
def main():
    book = AddressBook()

    while True:

        command = input("\nДоступні команди:\n"
                        "hello                           -- для допомоги\n"
                        "add [ім'я] [телефон]            -- для додавання контакту\n"
                        "change [ім'я] [індекс] [телефон]-- для зміни номера контакту\n"
                        "phone [ім'я]                    -- для отримання номера телефону\n"
                        "delete [ім'я]                   -- для видалення контакту\n"
                        "all                             -- для відображення всіх контактів\n"
                        "add-birthday [ім'я] [дата]      -- для додавання дня народження\n"
                        "show-birthday [ім'я]            -- для відображення дня народження\n"
                        "birthdays                       -- для відображення майбутніх днів народження\n"
                        "find-name [ім'я]                -- для пошуку за іменем\n"
                        "find-phone [телефон]            -- для пошуку за телефоном\n"
                        "find-birth [дата]               -- для пошуку за днем народження\n"
                        "add-notion [ім'я] [текст] [хештеги] -- для додавання нотатки\n"
                        "edit-notion [ім'я] [індекс] [новий текст] [нові хештеги] -- для редагування нотатки\n"
                        "delete-notion [ім'я] [індекс]   -- для видалення нотатки\n"
                        "add-hashtag [ім'я] [індекс нотатки] [хештег] -- для додавання хештегу до нотатки\n"
                        "remove-hashtag [ім'я] [індекс нотатки] [хештег] -- для видалення хештегу з нотатки\n"
                        "add-address [ім'я]              -- to add an address to a contact\n"
                        "edit-address [ім'я]             -- to edit the contacts's address\n"
                        "show-address [ім'я]             -- to show the contact's address\n"
                        "delete-address [ім'я]           -- to delete the contact's address\n"
                        "save [файл.json]                -- для збереження контактів у файл JSON\n"
                        "load [файл.json]                -- для завантаження контактів з файлу JSON\n"
                        "q /good bye/close/exit/quit     -- для виходу з програми\n"
                        "\nВведіть команду:").strip().lower()


        if command in ['q', 'good bye', 'close', 'exit', 'quit']:
            break
        elif command == 'hello':
            print("Привіт! Як я можу допомогти вам?")
        elif command == 'add':
            name = input("Введіть ім'я контакту: ").strip()
            phone = input("Введіть номер телефону: ").strip()
            record = Record(name)
            record.add_phone(phone)
            book.add_record(record)
            print(f"Контакт {name} додано успішно!")

        elif command.startswith("add-notion "):
            parts = command.split(" ", 3)
            if len(parts) >= 4:
                name, text, hashtags = parts[1], parts[2], parts[3]
                contact = book.find(name.lower())
                if contact:
                    contact.add_notion(text, hashtags)
                    print(f"Нотатка додана до контакту {name}.")
                else:
                    print("Контакт не знайдено.")
            else:
                print("Недостатньо аргументів. Використовуйте формат: add-notion [ім'я] [текст] [хештеги]")

        elif command.startswith("find-notions "):
            hashtag = command.split(" ", 1)[1]
            results = book.find_by_notion_or_hashtag(hashtag)
            if results:
                print(f"Знайдені контакти з нотатками, що містять '#{hashtag}':")
                for result in results:
                    for notion in result.notions:
                        if hashtag in notion.hashtags:
                            print(f"{result.name.value}: {notion.text} Хештеги: {' '.join(notion.hashtags)}")
            else:
                print(f"Нотатки з '#{hashtag}' не знайдено.")

        elif command.startswith("sort-by-hashtag "):
            hashtag = command.split(" ", 1)[1]
            sorted_contacts = book.sort_by_hashtag(hashtag)
            if sorted_contacts:
                print(f"Контакти відсортовані за '#{hashtag}':")
                for contact_name in sorted_contacts:
                    print(contact_name)
            else:
                print(f"Контакти з '#{hashtag}' не знайдено.")

        elif command == 'change':
            name = input("Введіть ім'я контакту: ").strip().lower()
            if name in book.data:
                contact = book.data[name]
                if not contact.phones:
                    phone = input("Введіть номер телефону: ").strip()
                    contact.add_phone(phone)
                else:
                    contact.display_phones()
                    old_phone_index = input("Введіть індекс номеру телефону, який хочете змінити: ")
                    new_phone = input("Введіть новий номер телефону: ").strip()
                    contact.edit_phone(old_phone_index, new_phone)
            else:
                print("Контакт не знайдено!")

        elif command.startswith("edit-notion "):
            parts = command.split(" ", 4)
            if len(parts) >= 5:
                name, index, new_text, new_hashtags = parts[1], parts[2], parts[3], parts[4]
                contact = book.find(name.lower())
                if contact:
                    contact.edit_notion(int(index), new_text, new_hashtags)
                    print("Нотатку успішно змінено.")
                else:
                    print("Контакт не знайдено.")
            else:
                print("Недостатньо аргументів. Використовуйте формат: edit-notion [ім'я] [індекс] [новий текст] [нові хештеги]")

        elif command.startswith("delete-notion "):
            parts = command.split(" ", 3)
            if len(parts) == 3:
                name, index = parts[1], parts[2]
                contact = book.find(name.lower())
                if contact:
                    contact.delete_notion(int(index))
                    print("Нотатку успішно видалено.")
                else:
                    print("Контакт не знайдено.")
            else:
                print("Недостатньо аргументів. Використовуйте формат: delete-notion [ім'я] [індекс]")

        elif command.startswith("add-hashtag "):
            parts = command.split(" ", 3)
            if len(parts) == 4:
                name, notion_index, hashtag = parts[1], parts[2], parts[3]
                contact = book.find(name.lower())
                if contact:
                    contact.add_hashtag_to_notion(int(notion_index), hashtag)
                    print(f"Хештег #{hashtag} додано до нотатки.")
                else:
                    print("Контакт не знайдено.")
            else:
                print("Недостатньо аргументів. Використовуйте формат: add-hashtag [ім'я] [індекс нотатки] [хештег]")

        elif command.startswith("remove-hashtag "):
            parts = command.split(" ", 3)
            if len(parts) == 4:
                name, notion_index, hashtag = parts[1], parts[2], parts[3]
                contact = book.find(name.lower())
                if contact:
                    contact.remove_hashtag_from_notion(int(notion_index), hashtag)
                    print(f"Хештег #{hashtag} видалено з нотатки.")
                else:
                    print("Контакт не знайдено.")
            else:
                print("Недостатньо аргументів. Використовуйте формат: remove-hashtag [ім'я] [індекс нотатки] [хештег]")

        elif command == 'phone':
            name = input("Введіть ім'я контакту: ").strip().lower()
            if name in book.data:
                print(f"Номер(и) телефону для {book.data[name].name.value}: {', '.join([str(phone) for phone in book.data[name].phones])}")
            else:
                print("Контакт не знайдено!")

        elif command == 'delete':
            name = input("Введіть ім'я контакту: ").strip().lower()
            if name in book.data:
                del_contact_name = book.data[name].name.value
                book.delete(name)
                print(f"Контакт {del_contact_name} видалено успішно!")
            else:
                print("Контакт не знайдено!")

        elif command == 'all':
            for record in book.data.values():
                print(record)

        elif command == 'all-names':
            existing_names = book.all_names()
            if existing_names:
                print("Existing contact names:")
                for name in existing_names:
                    print(name)
            else:
                print("No contacts found.")

        elif command == 'add-birthday':
            name = input("Введіть ім'я контакту: ").strip().lower()
            birthday = input("Введіть день народження (ДД.ММ.РРРР): ").strip()
            if name in book.data:
                book.data[name].add_birthday(birthday)
                print(f"День народження успішно додано для контакту {book.data[name].name.value}!")
            else:
                print("Контакт не знайдено!")

        elif command == 'show-birthday':
            name = input("Введіть ім'я контакту: ").strip().lower()
            if name in book.data:
                print(f"День народження для {book.data[name].name.value}: {book.data[name].show_birthday()}")
            else:
                print("Контакт не знайдено!")

        elif command == 'birthdays':
            upcoming_birthdays = book.birthdays()
            print("\nМайбутні дні народження:")
            for name in upcoming_birthdays:
                contact = book.find(name)
                if contact:
                    phone_number = ", ".join(str(phone) for phone in contact.phones) if contact.phones else "Немає номеру телефону"
                    print(f"День народження {name} буде на {contact.birthday}, номер для дзвінка {phone_number}")
                else:
                    print(f"Контакт для {name} не знайдено")

        elif command == 'find-name':
            name_to_find = input("Введіть ім'я для пошуку: ")
            found_contacts = Find.find_by_name(book, name_to_find)
            if found_contacts:
                print("Знайдені контакти:")
                for contact in found_contacts:
                    print(contact)
            else:
                print("Контакти не знайдено.")

        elif command == 'find-phone':
            phone_to_find = input("Введіть номер телефону для пошуку: ")
            found_contacts = Find.find_by_phone(book, phone_to_find)
            if found_contacts:
                print("Знайдені контакти:")
                for contact in found_contacts:
                    print(contact)
            else:
                print("Контакти не знайдено.")

        elif command == 'find-birth':
            birthday_to_find = input("Введіть день народження для пошуку (дд.мм.рррр): ")
            found_contacts = Find.find_by_birthday(book, birthday_to_find)
            if found_contacts:
                print("Знайдені контакти:")
                for contact in found_contacts:
                    print(contact)
            else:
                print("Контакти не знайдено.")

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

        elif command == 'add-address':
            name = input("Enter the name of the contact you want to add the address to: ")
            name_key = name.lower()
            if name_key in book:
                address = input("Enter the address: ").strip()
                record = book[name_key]
                record.add_address(address)
                print(f"Address {address} added to contact {name} successfully!")
            else:
                print(f"Contact {name} not found.")

        elif command == "show-address":
            name = input("Enter the name of the contact whose address you want to see: ")
            name_key = name.lower()
            if name_key in book:
                record = book[name_key]
                if record.address:
                    print(record.address.show_address(record.name.value))
                else:
                    print("Address for this contact has not been added yet or has been deleted")
            else:
                print("Contact not found")

        elif command == "edit-address":
            name = input("Enter the name of the contact whose address you want to change: ")
            name_key = name.lower()
            if name_key in book:
                record = book[name_key]
                if record.address:
                    new_address = input("Enter the new address: ")
                    result = book.edit_address(name, new_address)
                    if result is not None:
                        print(result)
                else:
                    print(f"No address has been added to {name} yet.")

        elif command == "delete-address":
            name = input("Enter the name of the contact whose address you want to delete: ")
            name_key = name.lower()
            if name_key in book:
                record = book[name_key]
                if record.address:
                    record.delete_address(record.address.show_address(name))
                    print(f"Address for {name} has been successfully deleted.")
                else:
                    print(f"No address was provided for {name}.")
            else:
                print(f"Contact {name} not found.")

        elif command == 'save':
            while True:
                filename = input("Введіть ім'я файлу для збереження (наприклад, contacts.json): ").strip()
                if not filename:
                    print("Не введено ім'я файлу. Використовується стандартне ім'я 'contacts_book.json'.")
                    filename = "contacts_book.json"
                try:
                    book.save_to_json(filename)
                    print(f"Контакти успішно збережено у файлі {filename}.")
                    break
                except Exception as e:
                    print(f"Виникла помилка при збереженні файлу: {e}.")

        elif command == 'load':
            filename = input("Введіть ім'я файлу для завантаження (наприклад, contacts.json): ").strip()
            book.load_from_json(filename)
            print("Контакти успішно завантажено!")

        else:
            print("\n Неправильна команда. \nБудь ласка, спробуйте ще раз.")


if __name__ == "__main__":
    main()