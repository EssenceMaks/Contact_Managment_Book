class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value.lower()] = record

    def find_by_notion_or_hashtag(self, search_term):
        results = []
        for record in self.data.values():
            if any(search_term in notion.value for notion in record.notions) or any(search_term in hashtag for notion in record.notions for hashtag in notion.hashtags):
                results.append(record)
        return results

    def save_to_json(self, filename):
        with open(filename, 'w') as f:
            json.dump([{
                "name": record.name.value,
                "phones": [str(phone) for phone in record.phones],
                "birthday": str(record.birthday) if record.birthday else None,
                "notions": [{"text": notion.value, "hashtags": notion.hashtags} for notion in record.notions]
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
                    birthday = item.get("birthday")
                    if birthday and birthday != 'None':
                        record.add_birthday(birthday)
                    for notion_item in item.get("notions", []):
                        record.add_notion(notion_item["text"])
                    self.add_record(record)
            print(f"Дані успішно завантажено з {filename}!")
        except FileNotFoundError:
            print(f"Файл '{filename}' не знайдено.")
        except json.JSONDecodeError:
            print(f"Помилка декодування JSON з файлу '{filename}'.")

# Example usage for testing
book = AddressBook()
record = Record("Jane Doe")
record.add_phone("0987654321")
record.add_notion("Meeting tomorrow #urgent")
book.add_record(record)
filename = "contacts_book.json"

# Save to JSON
book.save_to_json(filename)

# Clear the address book and load from JSON
book = AddressBook()
book.load_from_json(filename)

# Display loaded records to verify
for rec in book.data.values():
    print(rec)
class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value.lower()] = record

    def find_by_notion_or_hashtag(self, search_term):
        results = []
        for record in self.data.values():
            if any(search_term in notion.value for notion in record.notions) or any(search_term in hashtag for notion in record.notions for hashtag in notion.hashtags):
                results.append(record)
        return results

    def save_to_json(self, filename):
        with open(filename, 'w') as f:
            json.dump([{
                "name": record.name.value,
                "phones": [str(phone) for phone in record.phones],
                "birthday": str(record.birthday) if record.birthday else None,
                "notions": [{"text": notion.value, "hashtags": notion.hashtags} for notion in record.notions]
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
                    birthday = item.get("birthday")
                    if birthday and birthday != 'None':
                        record.add_birthday(birthday)
                    for notion_item in item.get("notions", []):
                        record.add_notion(notion_item["text"])
                    self.add_record(record)
            print(f"Дані успішно завантажено з {filename}!")
        except FileNotFoundError:
            print(f"Файл '{filename}' не знайдено.")
        except json.JSONDecodeError:
            print(f"Помилка декодування JSON з файлу '{filename}'.")

