import logging
import pandas
import os
import datetime as dt
import sqlite3
import click

@click.group()
def cli():
    pass


conn = sqlite3.connect("corona\\data\\coronavirus.db")
cursor = conn.cursor()

try:
    cursor.execute("""CREATE TABLE patients(first_name text, last_name text, birth_date text, phone text, document_type text, document_id text)""")
except sqlite3.OperationalError:
    pass

logger_error = logging.getLogger("error")
logger = logging.getLogger("success")

logger_error.setLevel(logging.DEBUG)
logger.setLevel(logging.DEBUG)

handler1 = logging.FileHandler("corona\\logs\\error_log.txt", 'a')
handler2 = logging.FileHandler("corona\\logs\\patient_log.txt", 'a')

formatter = logging.Formatter("%(filename)s[LINE:%(lineno)d]# %(levelname)-8s [%(asctime)s]  %(message)s")

handler1.setFormatter(formatter)
handler2.setFormatter(formatter)

logger_error.addHandler(handler1)
logger.addHandler(handler2)


def my_logging_decorator(func):

    def wrapper(self, *args):
        try:
            func(self, *args)
        except ValueError:
            logger_error.error("Wrong Argument")
            raise ValueError
        except TypeError:
            logger_error.error("Wrong Argument Type")
            raise TypeError
        except AttributeError:
            logger_error.error("Private Attribute")
            raise AttributeError

        if len(args) == 6:
            logger.debug("Patient %s %s was created" % (args[0], args[1]))
        elif len(args) == 2:
            logger.debug("Attribute %s was changed to %s" % (args[0], str(args[1])))
        elif not args:
            logger.debug("Patient %s %s was saved" % (self.first_name, self.last_name))
            
        handler1.close()
        handler2.close()

    return wrapper


class Patient:

    

    path = "corona\\data\\coronavirus.csv"

    @my_logging_decorator
    def __init__(self, firstname, secondname, date_of_birth, phone, document_type, document_id):

        if date_of_birth == None or phone == None or document_type == None or document_id == None:
            raise ValueError

        if not isinstance(firstname, str):
            raise TypeError

        if not firstname.isalpha():
            raise ValueError

        if not isinstance(secondname, str):
            raise TypeError

        if not secondname.isalpha():
            raise ValueError

        if not isinstance(date_of_birth, int) and not isinstance(date_of_birth, str):
            raise TypeError

        if str(date_of_birth).isalpha():
            raise ValueError

        if not isinstance(phone, int) and not isinstance(phone, str):
            raise TypeError

        if str(phone).isalpha():
            raise ValueError

        if not isinstance(document_type, str):
            raise TypeError

        if not isinstance(document_id, str) and not isinstance(document_id, int):
            raise TypeError

        if str(document_id).isalpha():
            raise ValueError
                
        self.first_name = str(firstname).capitalize()
        self.last_name = str(secondname).capitalize()

        date = ""
        for i in str(date_of_birth):
            if i in "0123456789":
                date += i
        if len(date) < 8:
            raise ValueError

        self.birth_date = dt.date(int(date[0:4]), int(date[4:6]), int(date[6::]))

        new_phone = ""
        i = 0
        while i < len(str(phone)):
            if phone[i] == '+' and phone[i+1] == "7":
                new_phone += '8'
                i += 1
            elif phone[i] == '0' or phone[i] == '1' or phone[i] == '2' or phone[i] == '3' or phone[i] == '4' or phone[i] == '5' or phone[i] == '6' or phone[i] == '7' or phone[i] == '8' or phone[i] == '9':
                new_phone += phone[i]
            i += 1
        self.phone = new_phone

        new_id = ""
        for i in str(document_id):
            if i == '0' or i == '1' or i == '2' or i == '3' or i == '4' or i == '5' or i == '6' or i == '7' or i == '8' or i == '9':
                new_id += i


        if document_type == "passport":
            if len(new_id) != 10:
                raise ValueError
            self.document_id = new_id

        elif document_type == "international passport":
            if len(new_id) != 9:
                raise ValueError
            self.document_id = new_id

        elif document_type == "driver license":
            if len(new_id) != 10:
                raise ValueError
            self.document_id = new_id

        else:
            raise ValueError

        self.document_type = document_type.lower()



    def create(firstname, secondname, date_of_birth, phone, doc, doc_number):
        return Patient(firstname, secondname, date_of_birth, phone, doc, doc_number)

    @my_logging_decorator
    def __setattr__(self, name, value):
        if name in self.__dict__:
            #firstname
            if name == "first_name":
                raise AttributeError

            #lastname
            elif name == "last_name":
                raise AttributeError

            #birth date
            elif name == "birth_date":
                if type(value) == float:
                    raise TypeError
                if value.isalpha() == True:
                    raise ValueError
                date = ""
                for i in str(value):
                    if i in "0123456789":
                        date += i
                if len(date) < 8:
                    raise ValueError

                self.__dict__[name] = dt.date(int(date[0:4]), int(date[4:6]), int(date[6::]))


            #phone
            elif name == "phone":
                if type(value) == float:
                    raise TypeError

                if str(value).isalpha() == True:
                    raise ValueError

                new_phone = ""
                i = 0
                while i < len(value):
                    if value[i] == '+' and value[i+1] == "7":
                        new_phone += '8'
                        i += 1
                    elif value[i] == '0' or value[i] == '1' or value[i] == '2' or value[i] == '3' or value[i] == '4' or value[i] == '5' or value[i] == '6' or value[i] == '7' or value[i] == '8' or value[i] == '9':
                        new_phone += value[i]
                    i += 1

                self.logger.debug("%s %s phone number was changed from %s to %s" % (self.first_name, self.last_name, self.phone, new_phone))
                self.__dict__[name] = new_phone


            #document type
            elif name == "document_type":
                if type(value) == float or type(value) == int:
                    self.logger_error.error("Wrong Argument Type: document type")
                    raise TypeError

                if value.lower() == "passport" or value.lower() == "international passport" or value.lower() == "driver license":
                    self.logger.debug("%s %s document was changed from %s to %s" % (self.first_name, self.last_name, self.document_type, value.lower()))
                    self.__dict__[name] = value.lower()
                else:
                    self.logger_error.error("Wrong Argument: document type")
                    raise ValueError


            #document id
            elif name == "document_id":
                if type(value) == float:
                    self.logger_error.error("Wrong Argument Type: document id")
                    raise TypeError

                id = ''.join(str(value).split())
                new_id = ""
                for i in id:
                    if i in "0123456789":
                        new_id += i

                if len(new_id) != 10 and len(new_id) != 9:
                    self.logger_error.error("Wrong Argumen: document id")
                    raise ValueError

                self.logger.debug("%s %s document number was changed from %s to %s" % (self.first_name, self.last_name, self.document_id, ''.join(str(value).split())))
                self.__dict__[name] = ''.join(str(value).split())
            
        else:
            self.__dict__[name] = value

    @my_logging_decorator
    def save(self):
        patient = (self.first_name, self.last_name, self.birth_date, self.phone, self.document_type, self.document_id)
        cursor.execute("INSERT INTO patients VALUES (?, ?, ?, ?, ?, ?)", patient)
        conn.commit()
       

    def __str__(self):
        return "firstname: %s, secondname: %s, date: %s, phone number: %s, document: %s, document number: %s" % (self.first_name, self.last_name, self.birth_date, self.phone, self.document_type, self.document_id)

@click.command()
@click.argument("first_name")
@click.argument("last_name")
@click.option("--birth_date", default = None, help = 'date format yyyy-mm-dd')
@click.option("--phone", default = None, help = "phone format 89030000000")
@click.option("--document_type", default = None, help = "passport, international passport, driver license")
@click.option("--document_number", default = None, help = "passport len = 10, international passport len = 9, driver license len = 10 (without space)")
def create(first_name, last_name, birth_date, phone, document_type, document_number):
    patient = Patient(first_name, last_name, birth_date, phone, document_type, document_number)
    patient.save()

@click.command()
@click.argument("value", default = 10)
def show(value):
    cursor.execute('SELECT * FROM patients')
    while value != 0:
        row = cursor.fetchone()
        if row == None:
            break
        print(Patient(row[0], row[1], row[2], row[3], row[4], row[5]))
        value -= 1

@click.command()
def count():
    cursor.execute('SELECT * FROM patients')
    counter = -1
    while True:
        row = cursor.fetchone()
        counter += 1
        if row == None:
            print(counter)
            break


# class PatientCollection:

#     def __init__(self, path_to_file):
#         self.path_to_file = path_to_file
#         self.conn_pc = sqlite3.connect(path_to_file)
#         self.cursor_pc = self.conn_pc.execute('SELECT * FROM patients')
#         self.count = -1


#     def __iter__(self):
#         return self

#     def __next__(self):
#         row = self.cursor_pc.fetchone()
#         if row is None or self.count == 0:
#             raise StopIteration
#         self.count -=1
#         return Patient(row[0], row[1], row[2], row[3], row[4], row[5])

#     def limit(self, count):
#         self.count = count
#         return self.__iter__()


path = "corona\\data\\coronavirus.db"

cli.add_command(create)
cli.add_command(show)
cli.add_command(count)


if __name__ == "__main__":
    cli()
