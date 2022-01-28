from faker import Faker
from faker.providers.phone_number import Provider
import phonenumbers
import random
import datetime
import csv
# from phonenumbers import carrier
from phonenumbers.phonenumberutil import (
    region_code_for_country_code
)

from utils import execution_time_calculator


class ExtraPhoneNumberProvider(Provider):
    """
    Add Extra Providers for phone number.
    """

    def egypt_phone_number(self):
        return f'+20 {self.msisdn()[2:]}'

    def kuwait_phone_number(self):
        return f'+965 {self.msisdn()[3:]}'

    def ksa_phone_number(self):
        return f'+966 {self.msisdn()[3:]}'


class ContactGenerator:

    def __init__(self):
        self._faker = Faker('en')
        self._ar_faker = Faker('ar')

    def _get_faker(self):
        """
        :return:
        """
        faker_choice = random.choice([self._faker, self._ar_faker])
        faker_choice.add_provider(ExtraPhoneNumberProvider)

        return faker_choice

    @staticmethod
    def _get_random_phone_country(faker):
        """
        :return:
        """
        choice = random.choice(
            [faker.egypt_phone_number(), faker.kuwait_phone_number(), faker.ksa_phone_number()]
        )
        return choice

    @staticmethod
    def _get_phone_number_country(num):
        """

        :param num:
        :return:
        """
        pn = phonenumbers.parse(num)

        return region_code_for_country_code(pn.country_code)

    def generate_contact(self, id):
        """
	    Will output csv file containg the following data
        
        id	name	    company	country	 phone	        mobile	          email	                           address
        1	Mina Samy   Xyz		KW		    		    965xxxxxxxx
        2	Ahmed	    Xyz		KW		    		    965xxxxxxxx
        5	Paul	    Xyz	    KW	     652-277-854	+965 7814296146	  delgadobrandon@example.org	   Default Address
        6   حكيم        Xyz	    EG	     959-312-088	+20 0181628459	  metwqqhtan@example.org	       Default Address


        :return:
        """
        faker = self._get_faker()
        mobile_number = self._get_random_phone_country(faker)
        phone_number_country_code = self._get_phone_number_country(mobile_number)

        return [
            id,
            faker.first_name(),
            'Xyz',
            phone_number_country_code,
            faker.phone_number(),
            mobile_number,
            faker.email(),
            'Default Address'
        ]


class FileHandler:
    """
    Output given contact list to csv file
    """

    def __init__(self, file_name='fake-contacts.csv'):
        self.file_name = file_name

    def write_to_csv(self, contact_list: list):
        with open('{}'.format(self.file_name), 'w+', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["id", "name", "company", "country", "phone", "mobile", "email", "address"])

            for i in range(len(contact_list)):
                writer.writerow(contact_list[i])


@execution_time_calculator
def generate_contacts(contact_generator, contact_numbers):
    print("Generating {} Contacts".format(contact_numbers))
    return [contact_generator.generate_contact(id) for id in range(1, contact_numbers + 1)]


if __name__ == '__main__':
    print("*" * 160)
    generation_time = datetime.datetime.now().strftime("%d-%m-%y %H-%M-%S")
    contact_num = 20

    contact_generator = ContactGenerator()
    csv_file_handle = FileHandler(file_name='generated_{}_contacts_{}.csv'.format(contact_num, generation_time))

    res = generate_contacts(contact_generator, contact_num)
    csv_file_handle.write_to_csv(res)
    print("*" * 160)
