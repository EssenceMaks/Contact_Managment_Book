from collections import UserDict

class Address:
    def __init__(self, address):
        self.addresses = [address]

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
    def __init__(self, name):
        super().__init__(name)

class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.address = None

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

    def add_record(self, name, record):
        self.data[name] = record

    def find(self, name):
        if name in self.data:
            return self.data[name]
        else:
            return "Record not found"

    def delete(self, name):
        if name in self.data:
            del self.data[name]
            return "Record deleted"
        else:
            return "Record not found"

    def edit_address(self, name, new_address):
        if name in self.data:
            record = self.data[name]
            if record.address:
                record.address.edit_address(new_address)
                print(f"Address for {name} has been successfully edited to {new_address}.")
            else:
                print(f"No address has been added to {name} yet.")
        else:
            print(f"Contact {name} not found.")

def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        
        elif command == "hello":
            print("How can I help you?")

        elif command == 'add':
            name = input("Enter contact name: ").strip()
            record = Record(name)
            book.add_record(name, record)
            print(f"Contact {name} added successfully!")

        elif command == 'add-address':
            name = input("Enter the name of the contact you want to add the address to: ")
            if name in book:
                address = input("Enter the address: ")
                record = book[name]
                record.add_address(address)
                print(f"Address {address} added to contact {name} successfully!")
            else:
                print(f"Contact {name} not found.")

        elif command == "show-address":
            name = input("Enter the name of the contact whose address you want to see: ")
            if name in book:
                record = book[name]
                if record.address:
                    print(record.address.show_address(record.name.value))
                else:
                    print("Address for this contact has not been added yet or has been deleted")
            else:
                print("Contact not found")

        elif command == "edit-address":
            name = input("Enter the name of the contact whose address you want to change: ")
            if name in book:
                record = book[name]
                if record.address:
                    new_address = input("Enter the new address: ")
                    result = book.edit_address(name, new_address)
                    if result is not None:
                        print(result)
                else:
                    print(f"No address has been added to {name} yet.")

        elif command == "delete-address":
            name = input("Enter the name of the contact whose address you want to delete: ")
            if name in book:
                record = book[name]
                if record.address:
                    record.delete_address(record.address.show_address(name))
                    print(f"Address for {name} has been successfully deleted.")
                else:
                    print(f"No address was provided for {name}.")
            else:
                print(f"Contact {name} not found.")

        else:
            print("Invalid command.")


if __name__ == "__main__":
    main()