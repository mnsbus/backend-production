import unittest
from entries import create_entry, determine_linetype
from entries import process_nameblock
from entries import FIELDS, VALIDATORS
from data_errors import DataValueError


class FieldValidatorCase(unittest.TestCase):
    def test_lengths(self):
        self.assertEqual(len(FIELDS), len(VALIDATORS))



class NameblockCases(unittest.TestCase):
    def test_nameblock_mi(self):
        result = process_nameblock(["Chas G. Roadrunner"])
        self.assertEqual(result, ["Chas G.", "Roadrunner"])


    def test_nameblock_no_mi(self):
        result = process_nameblock(["Chas Roadrunner"])
        self.assertEqual(result, ["Chas", "Roadrunner"])


    def test_nameblock_bad_mi(self):
        try:
            result = process_nameblock(["Chas G Roadrunner"])
        except DataValueError:
            pass
        else:
            self.fail("Did not see DataValueError")

    # need a more robust nameblock processor
    def test_nameblock_long_mi(self):
        try:
            result = process_nameblock(["Charles de la Renta"])
        except DataValueError:
            pass
        else:
            self.fail("Did not see DataValueError")

class LinetypeCases(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        # input elements
        self.elements0 = [
            'Lastname', 'Firstname', '(703)-742-0996', 'Blue', '10013'
        ]
        self.elements1 = [
            'Firstname Lastname', 'Red', '11237', '703 955 0373'
        ]
        self.elements2 = [
            'Firstname', 'Lastname', '10013', '646 111 0101', 'Green'
        ]
        self.elements3 = [
            'Booker T.', 'Washington', '87360', '373 781 7380', 'yellow'
        ]
        self.elements4 = [
            'Chandler', 'Kerri', '(623)-668-9293', 'pink', '123123121'
        ]
        self.elements5 = [
            'James Murphy', 'yellow', '83880', '018 154 6474'
        ]
        self.elements6 = [
            'asdfawefawea'
        ]
        # expected elements
        self.e_els0 = [
            'Lastname', 'Firstname', '(703)-742-0996', 'Blue', '10013'
        ]
        self.e_els1 = [
            'Firstname', 'Lastname', 'Red', '11237', '703 955 0373'
        ]
        self.e_els2 = [
            'Firstname', 'Lastname', '10013', '646 111 0101', 'Green'
        ]
        self.e_els3 = [
            'Booker T.', 'Washington', '87360', '373 781 7380', 'yellow'
        ]
        self.e_els4 = [
            'Chandler', 'Kerri', '(623)-668-9293', 'pink', '123123121'
        ]
        self.e_els5 = [
            'James', 'Murphy', 'yellow', '83880', '018 154 6474'
        ]
        self.e_els6 = None
        # expected indices
        self.e_indices0 = [3, 1, 0, 2, 4]
        self.e_indices1 = [2, 0, 1, 4, 3]
        self.e_indices2 = [4, 0, 1, 3, 2]
        self.e_indices3 = [4, 0, 1, 3, 2]
        self.e_indices4 = [3, 1, 0, 2, 4]
        self.e_indices5 = [2, 0, 1, 4, 3]
        self.e_indices6 = None
        # actual results
        self.r_els0, self.r_indices0 = determine_linetype(self.elements0)
        self.r_els1, self.r_indices1 = determine_linetype(self.elements1)
        self.r_els2, self.r_indices2 = determine_linetype(self.elements2)
        self.r_els3, self.r_indices3 = determine_linetype(self.elements3)
        self.r_els4, self.r_indices4 = determine_linetype(self.elements4)
        self.r_els5, self.r_indices5 = determine_linetype(self.elements5)

    def test_linetype_0e(self):
        self.assertEqual(self.e_els0, self.r_els0)

    def test_linetype_0i(self):
        self.assertEqual(self.e_indices0, self.r_indices0)

    def test_linetype_1e(self):
        self.assertEqual(self.e_els1, self.r_els1)

    def test_linetype_1i(self):
        self.assertEqual(self.e_indices1, self.r_indices1)

    def test_linetype_2e(self):
        self.assertEqual(self.e_els2, self.r_els2)

    def test_linetype_2i(self):
        self.assertEqual(self.e_indices2, self.r_indices2)

    def test_linetype_3e(self):
        self.assertEqual(self.e_els3, self.r_els3)

    def test_linetype_3i(self):
        self.assertEqual(self.e_indices3, self.r_indices3)

    def test_linetype_4e(self):
        self.assertEqual(self.e_els4, self.r_els4)

    def test_linetype_4i(self):
        self.assertEqual(self.e_indices4, self.r_indices4)

    def test_linetype_5e(self):
        self.assertEqual(self.e_els5, self.r_els5)

    def test_linetype_5i(self):
        self.assertEqual(self.e_indices5, self.r_indices5)

    def test_linetype_6(self):
        try:
            determine_linetype(self.elements6)
        except DataValueError:
            pass
        else:
            self.fail("Did not see DataValueError")



class CreateEntryCases(LinetypeCases):
    def test_create_entry3(self):
        er = {
                "color": "yellow",
                "firstname": "Booker T.",
                "lastname": "Washington",
                "phonenumber": "373-781-7380",
                "zipcode": "87360"
        }
        self.assertEquals(create_entry(self.r_els3, self.r_indices3), er)


    def test_create_entry4(self):
        try:
            create_entry(self.r_els4, self.r_indices4)
        except DataValueError:
            pass
        else:
            self.fail("Did not see DataValueError")


    def test_create_entry5(self):
        er = {
            "color": "yellow",
            "firstname": "James",
            "lastname": "Murphy",
            "phonenumber": "018-154-6474",
            "zipcode": "83880"
        }
        self.assertEquals(create_entry(self.r_els5, self.r_indices5), er)


if __name__ == '__main__':
    unittest.main()
