from collections import UserDict
from datetime import datetime, timedelta
from re import match


class WrongDateError(Exception):
    ...

class WrongPhoneFormat(Exception):
    ...


class NoDateError(Exception):
    ...

class Field:

    def __init__(self, value) -> None:
        self.value = value


    def __str__(self) -> str:
        return self.value


    def __repr__(self) -> str:
        return str(self)


class Name(Field):
    ...


class Phone(Field):
    def __init__(self, value = None):
        self._value = None
        self.value = value


    @property
    def value(self):
        return self._phone


    @value.setter
    def value(self, new_phone):
        r_data = r'\d{12}'
        data = match(r_data, new_phone)
        if data:
            self._phone = new_phone
        else:
            raise WrongPhoneFormat


class Birthday(Field):
    
    def __init__(self, value = None):
        self._value = None
        self.value = value


    @property
    def value(self):
        return self._birthday


    @value.setter
    def value(self, new_birthday):
        matched = r'^(\d{1,2}\.{1}\d{1,2}\.\d{4})$'
        data = match(matched, str(new_birthday))
        if data:
            self._birthday = new_birthday
        else:
            raise WrongDateError


class Record:

    def __init__(self, name: Name, phone: Phone = None, birthday : Birthday = None) -> None:
        self.name = name
        self.phones = []
        self.birthday = birthday
        self.phone = phone
        if phone:
            self.phones.append(phone)


    def add_phone(self, phone: Phone):
        if phone.value not in [p.value for p in self.phones]:
            self.phones.append(phone)
            return f"phone {phone} added to contact {self.name}"
        return f"{phone} is present in phones of contact {self.name}"


    def change_phone(self, old_phone: Phone, new_phone: Phone):
        for idx, p in enumerate(self.phones):
            if old_phone.value == p.value:
                self.phones[idx] = new_phone
                return f"old phone {old_phone.value} changeed to {new_phone.value}"
        return f"{old_phone.value} is not present in phones of contact {self.name}"


    def days_to_birthday(self):
        if self.birthday:
            birthday_date = self.birthday.value.split('.')
            current_date = datetime.now()
            datetime_birthday = datetime(year=current_date.year, month=int(birthday_date[1]), day=int(birthday_date[0]))
            days_left = datetime_birthday - current_date
            if days_left.days > 0:
                return days_left.days
            elif days_left.days < 0:
                datetime_birthday_2 = datetime(year=current_date.year + 1, month=int(birthday_date[1]), day=int(birthday_date[0]))
                result = datetime_birthday_2 - current_date
                return result.days
            else:
                return 'Tomorrow is your birthday'
        raise NoDateError


    def __str__(self) -> str:
        return f"{self.name}: {', '.join(str(p) for p in self.phones)}"


class AddressBook(UserDict):
    
    def __init__(self):
        super().__init__()
        

    def add_record(self, record: Record):
        self.data[str(record.name)] = record
        return f"Contact {record} add success"


    def __iter__(self):
        return iter(self.data)


    def __next__(self):
        if self._iter_index >= len(self.data):
            raise StopIteration
        key = list(self.data.keys())[self._iter_index]
        self._iter_index += 1
        return key


    def __iter__(self):
        self._iter_index = 0
        return self
    

    def __str__(self) -> str:
        return "\n".join(str(r) for r in self.data.values())