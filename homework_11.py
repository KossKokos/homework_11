from classes import AddressBook, Name, Phone, Record, Field, Birthday
from re import search

adress_book = AddressBook()

def input_error(func):
    def wrapper(*args):
        try:
            result = func(*args)
            return result
        except KeyError:
            return 'wrong name, please try again'
        except ValueError:
            return 'not a number, please try again'
        except IndexError:
            return 'Please enter some data'
    return wrapper


@input_error
def generator_records(*args):
    num = args[0]
    i = 0
    if len(adress_book) < int(num):
        return f'There are only {len(adress_book)} records in the adress_book, but you entered {num}'
    for val in adress_book.values():
        if i == int(num):
            break
        i += 1
        print(val)
    return 'Success!'


@input_error
def find_phone(*args):
    name = args[0]
    if name in adress_book.keys():
        rec: Record = adress_book.get(name)
        return f'name: {name}, phone: {rec.phones}'
    return f'name: {name} is not present'

    
@input_error
def show_all(*args):
    return adress_book


@input_error
def hello(*args):
    return 'How can I help you?'


@input_error
def change_phone(*args):
    name = Name(args[0])
    old_phone = Phone(args[1])
    new_phone = Phone(args[2])
    rec: Record = adress_book.get(str(name))
    if rec:
        rec.phone = new_phone
        return rec.change_phone(old_phone, new_phone)
    return f"No contact {name} in address book"

@input_error
def days_to_birthday(*args):
    name = args[0]
    if name in adress_book.keys():
        rec: Record = adress_book.get(str(name))
        data = rec.phones
        r_date = r'[\d\.]{1,}'
        find_date = search(r_date, data[0])
        if find_date.group() != None:
            return rec.days_to_birthday(find_date.group())
    return f"you haven't included date of birth or you have included wrong name"


@input_error
def add_command(*args):
    name = Name(args[0])
    rec: Record = adress_book.get(str(name))

    if rec:
        phone = Phone(args[1])
        rec.phone = phone
        return rec.add_phone(phone)
    
    if len(args) == 1:
        rec = Record(name)
        return adress_book.add_record(rec)
    
    elif len(args) == 2:
        phone = Phone(args[1])
        rec = Record(name)
        rec.phone = phone
        rec = Record(name, phone)
        return adress_book.add_record(rec)

    elif len(args) == 3:
        phone = Phone(args[1])
        birthday = Birthday(args[2])
        rec = Record(name)
        rec.phone = phone
        rec.birthday = birthday
        rec = Record(name, phone, birthday)
        return adress_book.add_record(rec)
    
    return 'something wrong'

def no_command(*args):
    return 'Unknown command'


dict_of_func = {
                'add': add_command,
                'change': change_phone, 
                'phone': find_phone, 
                'hello': hello, 
                'show_all': show_all,
                'birthday' : days_to_birthday,
                'generate' : generator_records
                }


@input_error
def parser(text: str) -> tuple[callable, tuple[str]]:
    func_name_num = text.split()
    if func_name_num[0] in dict_of_func.keys():
        return dict_of_func.get(func_name_num[0]), text.replace(func_name_num[0], '').strip().split()
    return no_command, text.replace(func_name_num[0], '').strip().split()
    

def main():
    while True:
        user_input = input('>>>')
        if user_input.lower() == 'exit' or user_input.lower() == 'close' or user_input.lower() == 'good bye':
            print('Bye!')
            break
        if user_input == '' or user_input == ' ':
            print(no_command(user_input))
            continue
        command, data = parser(user_input.lower())
        result = command(*data)
        print(result)


if __name__ == '__main__':
    main()