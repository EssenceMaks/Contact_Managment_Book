def command_line_helper(args=None):
    if args is None:
        return print("Щоб побачити меню команд введіть h або help")

    help = ("\nAvailable commands:\n"
            "\n"
            "hello                         -- to get assistance\n"
            "add [ім'я] [телефон]          -- to add a contact\n"
            "change [ім'я] [телефон]       -- to change a contact's phone number\n"
            "phone [ім'я]                  -- to get a contact's phone number\n"
            "delete [ім'я]                 -- to delete a contact\n"
            "all                           -- to show all contacts\n"
            "add-birthday [ім'я] [дата]    -- to add a birthday for a contact\n"
            "show-birthday [ім'я]          -- to show a contact's birthday\n"
            "birthdays                     -- to show upcoming birthdays\n"
            "find-name [ім'я]              -- to find a contact by name\n"
            "find-phone [телефон]          -- to find a contact by phone\n"
            "find-birth [дата]             -- to find a contact by birthday\n"
            "save [файл.json]              -- to save contacts to a JSON file\n"
            "load [файл.json]              -- to load contacts from a JSON file\n"
            "q /good bye/close/exit/quit   -- to exit the assistant\n"
            "h /help                       -- to help menu\n"
            "\n")

    return help


def main():
    print("Welcome to the assistant bot!")
    command_line_helper()
    while True:
        command = input("Enter a command: ")

        if command in ['q', 'good bye', 'close', 'exit', 'quit']:
            print("Good bay!")
            break

        elif command in ['h', 'help']:
            help = command_line_helper(command).strip().lower()
            print(help)

        elif command == 'add':
            name = input("Enter contact name: ").strip()
            phone = input("Enter phone number: ").strip()
            print(f"Contact {name} added successfully!")

        elif command == 'change':
            name = input("Enter contact name: ").strip().lower()

        elif command == 'phone':
            name = input("Enter contact name: ").strip().lower()

        elif command == 'delete':
            name = input("Enter contact name: ").strip().lower()

        elif command == 'all':
            pass

        elif command == 'add-birthday':
            name = input("Enter contact name: ").strip().lower()
            birthday = input("Enter birthday (DD.MM.YYYY): ").strip()

        elif command == 'show-birthday':
            name = input("Enter contact name: ").strip().lower()

        elif command == 'birthdays':
            print("\nUpcoming birthdays:")

        elif command == 'find-name':
            name_to_find = input("Enter name to find: ")

        elif command == 'find-phone':
            phone_to_find = input("Enter phone number to find: ")

        elif command == 'find-birth':
            birthday_to_find = input("Enter birthday to find (dd.mm.yyyy): ")

        elif command == 'save':
            filename = input(
                "Enter the filename to save to (e.g., contacts.json): ").strip()

        elif command == 'load':
            filename = input(
                "Enter the filename to load from (e.g., contacts.json): ").strip()

        elif command == 'hello':
            print("Hello! How can I assist you?")

        else:
            print("\n Incorrect command. \nPlease try correct command.")


if __name__ == "__main__":
    main()
