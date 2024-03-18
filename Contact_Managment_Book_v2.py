import json
import datetime
import re
from collections import UserDict
import difflib

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

class Email(Field):
    def __init__(self, value):
        self.pattern = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
        if self.pattern.match(value):
            self.value = value
        else:
            raise ValueError("Неіснуючий формат адреси електронної пошти.\nПовторіть спробу.")

class Birthday(Field):
    def __init__(self, value):
        try:
            self.value = datetime.datetime.strptime(value, '%d.%m.%Y')
        except ValueError:
            raise ValueError("Неправильний формат дати народження. Використовуйте формат ДД.ММ.РРРР.")

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

    @staticmethod
    def _validate_hashtags(hashtags):
        validated_hashtags = []
        pattern = re.compile(r"^#\w+$")
        for hashtag in hashtags:
            if pattern.match(hashtag):
                validated_hashtags.append(hashtag)
            else:
                raise ValueError("Неправильний формат хештегу.")
        return validated_hashtags
    
def get_valid_hashtags():
    while True:
        hashtags_input = input("Додайте хештеги: ")
        hashtags = hashtags_input.split()
        try:
            validated_hashtags = Notion._validate_hashtags(hashtags)
            return validated_hashtags
        except ValueError as e:
            print(e)
            print("Будь ласка, спробуйте ввести хештеги ще раз.")

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
        self.original_name = name
        self.name = Name(*name.split())
        self.phones = []
        self.email = None
        self.birthday = None
        self.notions = []
        self.address = None
        self.data = {}

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

    def add_email(self, email):
        self.email = Email(email)

    def show_email(self):
        if self.email:
            return str(self.email)
        else:
            return "не додана"

    def edit_email(self, new_email):
        if self.email is not None:
            self.email = Email(new_email)
        else:
            self.add_email(new_email)

    def delete_email(self, email_address):
        if self.email is not None:
            if self.email.value == email_address:
                self.email = None
                print("Електронну пошту успішно видалено!")
            else:
                print("Електронна пошта не знайдена.")
        else:
            print("Контакт не має електронної пошти для видалення.")

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def show_birthday(self):
        if self.birthday:
            return str(self.birthday)
        else:
            return "не додано"
    
    def add_notion(self, text, hashtags):
        hashtag_list = hashtags
        self.notions.append(Notion(text, hashtags))

    def edit_notion(self, index, new_text, new_hashtags):
        try:
            index = int(index)
            if 0 <= index < len(self.notions):
                self.notions[index] = Notion(new_text, new_hashtags)
                return "Нотатку успішно змінено."
            else:
                return "Неправильний індекс нотатки."
        except ValueError as e:
            print(e)

    def delete_notion(self, index):
        try:
            index = int(index)
            if 0 <= index < len(self.notions):
                del self.notions[index]
                return "Нотатку успішно видалено."
            else:
                print("Неправильний індекс нотатки.")
        except ValueError as e:
            print(e)

    def __str__(self):
        phones_str = '; '.join([str(phone) for phone in self.phones])
        birthday_str = self.show_birthday() if self.birthday else "не додано"
        notions_str = '; '.join([f"{notion.text} (Хештеги: {' '.join(notion.hashtags)})" for notion in self.notions])
        address_str = ', '.join(self.address.addresses) if hasattr(self, 'address') and self.address else "не додана"
        return f"Ім'я контакту: {self.original_name}, Телефони: {phones_str}, Електронна пошта: {self.show_email()}, День народження: {birthday_str}, Нотатки: {notions_str}, Адреса: {address_str}"

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
        with open(filename, 'w', encoding='utf-8') as f:
            json_data = []
            for record in self.data.values():
                record_data = {
                    'name': str(record.name),
                    'phones': [str(phone) for phone in record.phones],
                    "email": str(record.email) if record.email else None,
                    'birthday': str(record.birthday) if record.birthday else None,
                    'notions': [{'text': notion.text, 'hashtags': notion.hashtags} for notion in record.notions],
                    "addresses": record.address.addresses if record.address else []
                }
                json_data.append(record_data)
            json.dump(json_data, f, ensure_ascii=False, indent=4)
        return "Дані успішно збережено у файлі " + filename + "."

    def load_from_json(self, filename="contacts_book.json"):
        try:
            with open(filename, 'r', encoding= 'utf-8') as f:
                data = json.load(f)
                self.data.clear()
                for record_data in data:
                    record = Record(record_data["name"])
                    for phone in record_data.get("phones", []):
                        record.add_phone(phone)
                    email = record_data.get("email")
                    if email:
                        record.add_email(email)
                    birthday = record_data.get("birthday")
                    if birthday:
                        record.add_birthday(birthday)
                    for notion_data in record_data.get("notions", []):
                        record.add_notion(notion_data["text"], notion_data["hashtags"])
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

def command_line_helper(args=None):
    if args is None:
        return print("Щоб побачити меню команд введіть h або help")

    help = ("\nДоступні команди:\n"

            "hello                                                          -- для вітання з ботом\n"
            "h                                                              -- для допомоги\n"
            "help                                                           -- для допомоги\n"
            "add [ім'я] [телефон]                                           -- для додавання контакту\n"
            "change [ім'я] [індекс] [телефон]                               -- для зміни номера контакту\n"
            "phone [ім'я]                                                   -- для отримання номера телефону\n"
            "delete [ім'я]                                                  -- для видалення контакту\n"
            "all                                                            -- для відображення всіх контактів\n"
            "add-email [ім'я] [email]                                       -- для додавання електронної пошти\n"
            "show-email [ім'я]                                              -- для відображення електронної пошти\n"
            "edit-email [ім'я] [email]                                    -- для заміни електронної пошти\n"
            "delete-email [ім'я] [email]                                    -- для видалення електронної пошти\n"
            "add-birthday [ім'я] [дата]                                     -- для додавання дня народження\n"
            "show-birthday [ім'я]                                           -- для відображення дня народження\n"
            "birthdays                                                      -- для відображення майбутніх днів народження\n"
            "find-name [ім'я]                                               -- для пошуку за ім'ям\n"
            "find-phone [телефон]                                           -- для пошуку за телефоном\n"
            "find-birth [дата]                                              -- для пошуку за днем народження\n"
            "add-notion [ім'я] [текст] [хештеги]                            -- для додавання нотатки\n"
            "edit-notion [ім'я] [індекс] [новий текст] [нові хештеги]       -- для редагування нотатки\n"
            "delete-notion [ім'я] [індекс]                                  -- для видалення нотатки\n"
            "add-hashtag [ім'я] [індекс нотатки] [хештег]                   -- для додавання хештегу до нотатки\n"
            "remove-hashtag [ім'я] [індекс нотатки] [хештег]                -- для видалення хештегу з нотатки\n"
            "add-address [ім'я]                                             -- для додавання адреси\n"
            "show-address [ім'я]                                            -- для відображення адреси\n"
            "edit-address [ім'я]                                            -- для редагування адреси\n"
            "delete-address [ім'я]                                          -- для видалення адреси\n"
            "save [файл.json]                                               -- для збереження контактів у файл JSON\n"
            "load [файл.json]                                               -- для завантаження контактів з файлу JSON\n"
            "q /good bye/close/exit/quit                                    -- для виходу з програми\n"
            "\nВведіть команду:"
            "\n")
            

    return help
# _______________________________________________________________________________________________________________________________


def main():
    book = AddressBook()
    print("Ласкаво просимо! Вас вітає бот-помічник!")
    command_line_helper()

    while True:
      
        command = input("Введіть команду: ")

        if command in ['q', 'good bye', 'close', 'exit', 'quit']:
            break

        elif command in ['h', 'help']:
            help = command_line_helper(command).strip().lower()
            print(help)

        elif command == 'hello':
            print("Привіт! Як я можу допомогти вам?")
        
        # elif command == 'add':
        #     name = input("Введіть ім'я контакту: ").strip()
        #     phone = input("Введіть номер телефону: ").strip()
        #     record = Record(name)
        #     record.add_phone(phone)
        #     book.add_record(record)
        #     print(f"Контакт {name} додано успішно!")

        elif command == 'add':
            name = input("Введіть ім'я контакту: ").strip()
            name_match = name.lower()
            if name_match in book.data:
                print(f"Контакт з ім'ям '{name}' вже існує. Будь ласка, повторіть команду 'add' та введіть інше ім'я.")
            else:
                while True:
                    phone = input("Введіть номер телефону: ").strip()
                    if phone:
                        break
                record = Record(name)
                record.add_phone(phone)
                book.add_record(record)
                print(f"Контакт '{name}' додано успішно!")

                
        elif command == 'add-notion':
            name = input("Введіть ім'я контакту до якого ви б хотіли додати нотатку: ")
            name_key = name.lower()
            if name_key in book:
                text = input("Введіть текст: ")
                hashtags = get_valid_hashtags() 
                record = book[name_key]
                record.add_notion(text, hashtags)
                print("Нотатку успішно додано!")
            else:
                print(f"Контакт {name} не знайдено.")

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

        elif command.startswith("edit-notion"):
            name = input("Введіть ім'я контакту, в якого ви хочете змінити нотатку: ")
            name_key = name.lower()
            if name_key in book:
                record = book[name_key]
                if record.notions:
                    for i, notion in enumerate(record.notions):
                        print(f"{i}: {notion.text} - {' '.join(notion.hashtags)}")
                    index = input("Введіть номер нотатки, яку хочете змінити: ")
                    try:
                        index = int(index)
                        if 0 <= index < len(record.notions):
                            new_text = input("Введіть новий текст нотатки: ")
                            new_hashtags = input("Додайте нові хештеги: ")
                            record.edit_notion(index, new_text, new_hashtags.split())
                            print("Нотатку успішно змінено!")
                        else:
                            print("Неправильний номер нотатки.")
                    except ValueError:
                        print("Номер нотатки має бути числом.")
                else:
                    print("У цього контакту немає нотаток.")
            else:
                print(f"Контакт {name} не знайдено.")

        elif command.startswith("delete-notion"):
            name = input("Введіть ім'я контакту, в якого ви хочете видалити нотатку: ")
            name_key = name.lower()
            if name_key in book:
                record = book[name_key]
                if record.notions:
                    for i, notion in enumerate(record.notions):
                        print(f"{i}: {notion.text} - {' '.join(notion.hashtags)}")
                    index = input("Введіть номер нотатки для видалення: ")
                    try:
                        index = int(index)
                        if 0 <= index < len(record.notions):
                            record.delete_notion(index)
                            print("Нотатку успішно видалено!")
                        else:
                            print("Неправильний номер нотатки.")
                    except ValueError:
                        print("Номер нотатки має бути числом.")
                else:
                    print("У цього контакту немає нотаток.")
            else:
                print(f"Контакт {name} не знайдено.")

        elif command == 'add-hashtag':
            name = input("Введіть ім'я контакту до якого ви хотіли б додати хештег: ")
            name_key = name.lower()
            if name_key in book:
                record = book[name_key]
                if record.notions:
                    for i, notion in enumerate(record.notions):
                        print(f"{i}: {notion.text} - {' '.join(notion.hashtags)}")
                    index = input("Введіть номер нотатки, до якої хочете додати хештег: ")
                    try:
                        index = int(index)
                        if 0 <= index < len(record.notions):
                            new_hashtag = get_valid_hashtags()
                            record.notions[index].hashtags.extend(new_hashtag)
                            print("Хештег успішно додано!")
                        else:
                            print("Неправильний номер нотатки.")
                    except ValueError:
                        print("Номер нотатки має бути числом.")
                else:
                    print("У цього контакту немає нотаток.")
            else:
                print(f"Контакт {name} не знайдено.")

        elif command == 'remove-hashtag':
            name = input("Введіть ім'я контакту від якого ви хотіли б видалити хештег: ")
            name_key = name.lower()
            if name_key in book:
                record = book[name_key]
                if record.notions:
                    for i, notion in enumerate(record.notions):
                        print(f"{i}: {notion.text} - {' '.join(notion.hashtags)}")
                    index = input("Введіть номер нотатки, від якої хочете видалити хештег: ")
                    try:
                        index = int(index)
                        if 0 <= index < len(record.notions):
                            hashtag_to_remove = input("Введіть хештег для видалення: ")
                            if hashtag_to_remove in record.notions[index].hashtags:
                                record.notions[index].hashtags.remove(hashtag_to_remove)
                                print("Хештег успішно видалено!")
                            else:
                                print("Такий хештег не знайдено у вибраній нотатці.")
                        else:
                            print("Неправильний номер нотатки.")
                    except ValueError:
                        print("Номер нотатки має бути числом.")
                else:
                    print("У цього контакту немає нотаток.")
            else:
                print(f"Контакт {name} не знайдено.")

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
                
        # Цієї команди all-names немає в "Доступні команди:" - можливо вона взагалі не потрібна
        elif command == 'all-names':
            existing_names = book.all_names()
            if existing_names:
                print("Існуюючі імена контактів: ")
                for name in existing_names:
                    print(name)
            else:
                print("Контакти не знайдено.")
        
        elif command == 'add-email':
            name = input("Введіть ім'я контакту: ").strip().lower()
            email = input("Введіть адресу електронної пошти: ").strip()
            if name in book.data:
                try:
                    book.data[name].add_email(email)
                except ValueError:
                    print("Неіснуючий формат адреси електронної пошти.\nПовторіть спробу.")
                else:
                    print(f"Додано адресу електронної пошти для контакту {book.data[name].name.value}!")
            else:
                print("Контакт не знайдено!")

        elif command == 'show-email':
            name = input("Введіть ім'я контакту: ").strip().lower()
            if name in book.data:
                print(f"Адреса електронної пошти {book.data[name].name.value}: {book.data[name].show_email()}")
            else:
                print("Контакт не знайдено!")

        elif command == 'edit-email':
            name = input("Введіть ім'я контакту: ").strip().lower()
            if name in book.data:
                contact = book.data[name]
                if contact.email:
                    new_email = input("Введіть нову адресу електронної пошти: ").strip()
                    try:
                        contact.edit_email(new_email)
                    except ValueError:
                        print("Неіснуючий формат адреси електронної пошти.\nПовторіть спробу")
                    else:
                        print(f"Змінено адресу електронної пошти для контакту {book.data[name].name.value}!")
                else:
                    print("Контакт не має електронної адреси для редагування.")
            else:
                print("Контакт не знайдено!")

        elif command == "delete-email":
            name = input("Введіть ім'я контакту: ").strip().lower()
            if name in book:
                record = book[name]
                if record.email is not None:
                    email_to_delete = email
                    record.delete_email(email_to_delete)
                else:
                    print(f"Для {name} не надано електронної пошти.")
            else:
                print(f"Контакт {name} не знайдено!")

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
                print("Знайдені контакти: ")
                for contact in found_contacts:
                    print(contact)
            else:
                print("Контакти не знайдено.")

        elif command == 'find-phone':
            phone_to_find = input("Введіть номер телефону для пошуку: ")
            found_contacts = Find.find_by_phone(book, phone_to_find)
            if found_contacts:
                print("Знайдені контакти: ")
                for contact in found_contacts:
                    print(contact)
            else:
                print("Контакти не знайдено.")

        elif command == 'find-birth':
            birthday_to_find = input("Введіть день народження для пошуку (ДД.ММ.РРРР): ")
            found_contacts = Find.find_by_birthday(book, birthday_to_find)
            if found_contacts:
                print("Знайдені контакти: ")
                for contact in found_contacts:
                    print(contact)
            else:
                print("Контакти не знайдено.")

        elif command == 'find-name':
            name_to_find = input("Введіть ім'я, яке хочете знайти: ")
            found_contacts = Find.find_by_name(book, name_to_find)
            if found_contacts:
                print("Знайдені контакти: ")
                for contact in found_contacts:
                    print(contact)
            else:
                print("Контакт не знайдено.")

        # Ця command == 'find-phone' - дубль - необхідно видалити
        elif command == 'find-phone':
            phone_to_find = input("Enter phone number to find: ")
            found_contacts = Find.find_by_phone(book, phone_to_find)
            if found_contacts:
                print("Found contacts:")
                for contact in found_contacts:
                    print(contact)
            else:
                print("Контакти не знайдено.")

        # Ця command == 'find-birth' - дубль - необхідно видалити
        elif command == 'find-birth':
            birthday_to_find = input("Enter birthday to find (dd.mm.yyyy): ")
            found_contacts = Find.find_by_birthday(book, birthday_to_find)
            if found_contacts:
                print("Found contacts:")
                for contact in found_contacts:
                    print(contact)
            else:
                print("Контакти не знайдено.")

        elif command == 'add-address':
                name = input("Enter the name of the contact you want to add the address to: ")
                name_key = name.lower()
                if name_key in book:
                    while True:
                        address = input("Enter the address: ").strip()
                        if len(address) > 120:
                            print("Address exceeds the maximum allowed length of 120 symbols. Please try again.")
                        else:
                            record = book[name_key]
                            record.add_address(address)
                            print(f"Address {address} added to contact {name} successfully!")
                            break
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
                print("Контакт не знайдено.")

        elif command == "edit-address":
            name = input("Enter the name of the contact whose address you want to change: ")
            name_key = name.lower()
            if name_key in book:
                record = book[name_key]
                if record.address:
                    new_address = input("Enter the new address: ")
                    book.edit_address(name, new_address)
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
                print(f"Контакт {name} не знайдено.")

        elif command == 'save':
            while True:
                filename = input("Введіть ім'я файлу для збереження (наприклад, contacts.json): ").strip()
                if not filename:
                    print("\n Не введено ім'я файлу. \n Використовується стандартне ім'я 'contacts_book.json'.")
                    filename = "contacts_book.json"
                try:
                    book.save_to_json(filename)
                    print(f"\n Контакти успішно збережено у файлі {filename}.")
                    break
                except Exception as e:
                    print(f"Виникла помилка при збереженні файлу: {e}.")

        elif command == 'load':
            filename = input("Введіть ім'я файлу для завантаження (наприклад, contacts.json): ").strip()
            book.load_from_json(filename)
            print("Контакти успішно завантажено!")

        else:
            print("\n Неправильна команда.")
            # print("\n Неправильна команда. \nБудь ласка, спробуйте ще раз.")
            # Цей print був до того, як з'явилися повідомлення з підказками для невірних команд - його та цей коментар можна видаляти

        # Словник доступних команд
        available_commands = {
            "hello": "для вітання з ботом",
            "h": "для допомоги",
            "help": "для допомоги",
            "add": "для додавання контакту",
            "change": "для зміни номера контакту",
            "phone": "для отримання номера телефону",
            "delete": "для видалення контакту",
            "all": "для відображення всіх контактів",
            "add-email": "для додавання електронної пошти",
            "show-email": "для відображення електронної пошти",

            "edit-email": "для заміни електронної пошти",

            "delete-email": "для видалення електронної пошти",
            "add-birthday": "для додавання дня народження",
            "show-birthday": "для відображення дня народження",
            "birthdays": "для відображення майбутніх днів народження",
            "find-name": "для пошуку за ім'я",
            "find-phone": "для пошуку за телефоном",
            "find-birth": "для пошуку за днем народження",
            "add-notion": "для додавання нотатки",
            "edit-notion": "для редагування нотатки",
            "delete-notion": "для видалення нотатки",
            "add-hashtag": "для додавання хештегу до нотатки",
            "remove-hashtag": "для видалення хештегу з нотатки",
            "add-address": "для додавання адреси",
            "show-address": "для відображення адреси",

            "edit-address": "для редагування адреси",

            "delete-address": "для видалення адреси",
            "save": "для збереження контактів у файл JSON",
            "load": "для завантаження контактів з файлу JSON",
            "good bye": "для виходу з програми",
            "q": "для виходу з програми",
            "quit": "для виходу з програми",
            "close": "для виходу з програми",
            "exit": "для виходу з програми"
        }

        def suggest_command(user_input):

            matches = [command for command in available_commands.keys() if command.startswith(user_input)]
            if len(matches) == 1:
                return f"Можливо, ви мали на увазі команду: {matches[0]}?\nБудь ласка, спробуйте ще раз."
            elif matches:
                return f"Можливо, ви мали на увазі одну з цих команд: {', '.join(matches)}?\nБудь ласка, спробуйте ще раз."
            else:
                return "Вибачте, я не зрозумів вашу команду. Спробуйте ще раз або введіть 'h' або 'help' для допомоги."


        if command in available_commands:
            pass
        else:
            suggestion = suggest_command(command)
            print(suggestion)


if __name__ == "__main__":
    main()