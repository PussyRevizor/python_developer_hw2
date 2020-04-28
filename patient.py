import logging
import pandas
import os
import datetime as dt


class Patient:

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

    path = "corona\\data\\coronavirus.csv"

    def __init__(self, firstname, secondname, date_of_birth, phone, document_type, document_id):


        if type(firstname) == int or type(firstname) == float:
            self.logger_error.error("Wrong Argument Type: firstname")
            raise TypeError

        if firstname.isalpha() != True:
            self.logger_error.error("Wrong Argument: firstname")
            raise ValueError

        if type(secondname) == int or type(secondname) == float:
            self.logger_error.error("Wrong Argument Type: lastname")
            raise TypeError

        if secondname.isalpha() != True:
            self.logger_error.error("Wrong Argument: lastname")
            raise ValueError


        if type(date_of_birth) == float:
            self.logger_error.error("Wrong Argument Type: birth date")
            raise TypeError

        if str(date_of_birth).isalpha() == True:
            self.logger_error.error("Wrong Argument: birth date")
            raise ValueError

        if type(phone) == float:
            self.logger_error.error("Wrong Argument Type: phone")
            raise TypeError

        if str(phone).isalpha() == True:
            self.logger_error.error("Wrong Argument: phone")
            raise ValueError

        if type(document_type) == float:
            self.logger_error.error("Wrong Argument Type: document type")
            raise TypeError

        if type(document_id) == float:
            self.logger_error.error("Wrong Argument Type: document id")
            raise TypeError
                
        self.first_name = str(firstname).capitalize()
        self.last_name = str(secondname).capitalize()

        date = ""
        for i in str(date_of_birth):
            if i == '0' or i == '1' or i == '2' or i == '3' or i == '4' or i == '5' or i == '6' or i == '7' or i == '8' or i == '9':
                date += i
        if len(date) < 8:
            self.logger_error.error("Wrong Argument: date")
            raise ValueError

        self.birth_date = dt.datetime(int(date[0:4]), int(date[4:6]), int(date[6::]), 0, 0)

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

        #id = ''.join(str(document_id).split())
        new_id = ""
        for i in str(document_id):
            if i == '0' or i == '1' or i == '2' or i == '3' or i == '4' or i == '5' or i == '6' or i == '7' or i == '8' or i == '9':
                new_id += i


        if document_type == "passport":
            if len(new_id) != 10:
                self.logger_error.error("Wrong Argument: document id")
                raise ValueError
            self.document_id = new_id

        elif document_type == "international passport":
            if len(new_id) != 9:
                self.logger_error.error("Wrong Argument: document id")
                raise ValueError
            self.document_id = new_id

        elif document_type == "driver license":
            if len(new_id) != 10:
                self.logger_error.error("Wrong Argument: document id")
                raise ValueError
            self.document_id = new_id

        else:
            self.logger_error.error("Wrong Argument: document type")
            raise ValueError

        self.document_type = document_type.lower()

        self.logger.debug("Create patient %s %s" % (self.first_name, self.last_name))


    def create(firstname, secondname, date_of_birth, phone, doc, doc_number):
        return Patient(firstname, secondname, date_of_birth, phone, doc, doc_number)


    def __setattr__(self, name, value):
        if name in self.__dict__:
            #firstname
            if name == "first_name":
                self.logger_error.error("%s %s Firstname cannot be changed" % (self.first_name, self.last_name))
                raise AttributeError

            #lastname
            elif name == "last_name":
                self.logger_error.error("%s %s Secondname cannot be changed" % (self.first_name, self.last_name))
                raise AttributeError

            #birth date
            elif name == "birth_date":
                if type(value) == float:
                    self.logger_error.error("Wrong Argument Type: birth date")
                    raise TypeError
                if value.isalpha() == True:
                    self.logger_error.error("Wrong Argument: birth date")
                    raise ValueError
                date = ""
                for i in str(value):
                    if i == '0' or i == '1' or i == '2' or i == '3' or i == '4' or i == '5' or i == '6' or i == '7' or i == '8' or i == '9':
                        date += i
                if len(date) < 8:
                    self.logger_error.error("Wrong Argument: date")
                    raise ValueError

                self.logger.debug("%s %s date of birth was changed from %s to %s" % (self.first_name, self.last_name, self.birth_date, date))
                self.__dict__[name] = dt.datetime(int(date[0:4]), int(date[4:6]), int(date[6::]), 0, 0)


            #phone
            elif name == "phone":
                if type(value) == float:
                    self.logger_error.error("Wrong Argument Type: phone")
                    raise TypeError

                if str(value).isalpha() == True:
                    self.logger_error.error("Wrong Argument: phone")
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
                #if len(new_phone) != 11:
                 #   self.logger_error.error("Wrong Argument: phone")
                  #  raise Exception("ValueError")

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
                    if i == '0' or i == '1' or i == '2' or i == '3' or i == '4' or i == '5' or i == '6' or i == '7' or i == '8' or i == '9':
                        new_id += i

                if len(new_id) != 10 and len(new_id) != 9:
                    self.logger_error.error("Wrong Argumen: document id")
                    raise ValueError

                self.logger.debug("%s %s document number was changed from %s to %s" % (self.first_name, self.last_name, self.document_id, ''.join(str(value).split())))
                self.__dict__[name] = ''.join(str(value).split())
            
        else:
            self.__dict__[name] = value


    def save(self):
        df = pandas.DataFrame([[self.first_name, self.last_name, self.birth_date, self.phone, self.document_type, self.document_id]], columns = ["first_name", "last_name", "birth_date", "phone", "document_type", "document_id"])
        #df = pandas.DataFrame([[self.first_name, self.last_name, self.birth_date, self.phone, self.document_type, self.document_id]])
        if not os.path.isfile(self.path):
            df.to_csv(self.path, mode = 'w', index = False, header = None)
            self.logger.debug("File coronavirus.csv was created")
        else:
            df.to_csv(self.path, mode = 'a', index = False, header = None)
        self.logger.debug("Patient %s %s was added to coronavirus.csv" % (self.first_name, self.last_name))


    def __str__(self):
        return "firstname: %s, secondname: %s, date: %s, phone number: %s, document: %s, document number: %s" % (self.first_name, self.last_name, self.birth_date, self.phone, self.document_type, self.document_id)


    def __del__(self):
        self.handler1.close()
        self.handler2.close()




class PatientCollection:

    def __init__(self, path_to_file):
        self.path_to_file = path_to_file
        self.counter = -1


    def __iter__(self):
        return self


    def __next__(self):
        df = pandas.read_csv(self.path_to_file, names = ["first_name", "last_name", "birth_date", "phone", "document_type", "document_id"])
        self.count = df["first_name"].count() - 1
        try:
            if self.counter < self.count:
                self.counter += 1
                return Patient(str(df["first_name"][self.counter]), str(df["last_name"][self.counter]), str(df["birth_date"][self.counter]), str(df["phone"][self.counter]), str(df["document_type"][self.counter]), str(df["document_id"][self.counter]))
            else:
                self.counter = -1
                raise StopIteration
        except KeyError:
            self.counter = -1
            raise StopIteration


    def limit(self, count):
        self.count = count
        return self.__iter__()