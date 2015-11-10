import unittest
from test_entries import LinetypeCases
from utils import extract_digits, preprocess_line
from utils import validate_color, validate_mi_or_raise, validate_name
from utils import validate_phonenumber, validate_phonenumber_or_raise
from utils import validate_zipcode, validate_zipcode_or_raise
from data_errors import DataValueError

class ExtractDigitsCases(unittest.TestCase):
    def test_extract_digits0(self):
        self.assertEqual(
            extract_digits('ds03453fsdfs4506kgfdgdfg'),
            '034534506'
        )

    def test_extract_digits1(self):
        self.assertEqual(
            extract_digits('03453'),
            '03453'
        )

    def test_extract_digits2(self):
        self.assertEqual(
            extract_digits('a0b3c4d5e3f'),
            '03453'
        )

    def test_extract_digits4(self):
        self.assertEqual(
            extract_digits('a0b3c4d5e3f'),
            '03453'
        )

    def test_extract_digits5(self):
        try:
            extract_digits(03453)
        except TypeError:
            pass
        else:
            self.fail("Expected TypeError")



class PreProcessLineCases(LinetypeCases):
    def test_ppl_0(self):
        self.l0 = 'Lastname, Firstname, (703)-742-0996, Blue, 10013    '
        self.assertEqual(preprocess_line(self.l0), self.elements0)

    def test_ppl_1(self):
        self.l1 = 'Firstname Lastname, Red,       11237, 703 955 0373'
        self.assertEqual(preprocess_line(self.l1), self.elements1)

    def test_ppl_2(self):
        self.l2 = '     Firstname, Lastname, 10013, 646 111 0101, Green'
        self.assertEqual(preprocess_line(self.l2), self.elements2)

    def test_ppl_3(self):
        self.l3 = 'Booker T.,    Washington,     87360,    373 781 7380, yellow'
        self.assertEqual(preprocess_line(self.l3), self.elements3)

    def test_ppl_4(self):
        self.l4 = 'Chandler, Kerri, (623)-668-9293, pink, 123123121'
        self.assertEqual(preprocess_line(self.l4), self.elements4)

    def test_ppl_5(self):
        self.l5 = 'James Murphy, yellow, 83880, 018 154 6474'
        self.assertEqual(preprocess_line(self.l5), self.elements5)

    def test_ppl_6(self):
        self.l6 = 'asdfawefawea'
        self.assertEqual(preprocess_line(self.l6), ['asdfawefawea'])



class ValidatorCases(unittest.TestCase):
    def test_validate_color0(self):
        self.assertEqual(validate_color('not a color'), 'not a color')

    def test_validate_color1(self):
        self.assertEqual(validate_color('not a 5olor'), None)

    def test_validate_color2(self):
        try:
            validate_color(55555)
        except TypeError:
            pass
        else:
            self.fail("Expected TypeError")

    def test_validate_name0(self):
        self.assertEqual(validate_name('Chas Good'), 'Chas Good')

    def test_validate_name1(self):
        self.assertEqual(validate_name('Chas 5ood'), None)

    def test_validate_name2(self):
        self.assertEqual(validate_name('C.A. Capricorn'), 'C.A. Capricorn')

    def test_validate_name3(self):
        self.assertEqual(validate_name('Jean-Michel Lo'), 'Jean-Michel Lo')

    def test_validate_zipcode0(self):
        self.assertEqual(validate_zipcode('90210'), '90210')

    def test_validate_zipcode1(self):
        self.assertEqual(validate_zipcode('902106'), None)

    def test_validate_zipcode2(self):
        try:
            validate_zipcode(90210)
        except TypeError:
            pass
        else:
            self.fail("Expected TypeError")

    def test_validate_zipcode_or_raise0(self):
        self.assertEqual(validate_zipcode_or_raise('90210'), '90210')

    def test_validate_zipcodeor_raise1(self):
        try:
            validate_zipcode_or_raise('902106')
        except DataValueError:
            pass
        else:
            self.fail("Expected DataValueError")

    def test_validate_zipcodeor_raise2(self):
        try:
            validate_zipcode_or_raise(90210)
        except TypeError:
            pass
        else:
            self.fail("Expected Typeerror")

    def test_validate_phonenumber0(self):
        self.assertEqual(validate_phonenumber('7153456434'), '7153456434')

    def test_validate_phonenumber1(self):
        self.assertEqual(validate_phonenumber('902106'), None)

    def test_validate_phonenumber2(self):
        try:
            validate_phonenumber(7153456434)
        except TypeError:
            pass
        else:
            self.fail("Expected Typeerror")

    def test_validate_phonenumber_or_raise0(self):
        self.assertEqual(
            validate_phonenumber_or_raise('715-345-6434'), '715-345-6434'
        )

    def test_validate_phonenumberor_raise1(self):
        try:
            validate_phonenumber_or_raise('902106')
        except DataValueError:
            pass
        else:
            self.fail("Expected DataValueError")

    def test_validate_phonenumberor_raise2(self):
        try:
            validate_phonenumber_or_raise(90210)
        except TypeError:
            pass
        else:
            self.fail("Expected Typeerror")

    def test_validate_phonenumber_or_raise3(self):
        self.assertEqual(
            validate_phonenumber_or_raise('(716) 543-5655'), '716-543-5655'
        )

    def test_validate_phonenumber_or_raise4(self):
        try:
            validate_phonenumber_or_raise('(716) 543-56556')
        except DataValueError:
            pass
        else:
            self.fail("Expected DataValueError")


    def test_validate_mi_or_raise0(self):
        self.assertEqual(validate_mi_or_raise("N."), "N.")

    def test_validate_mi_or_raise1(self):
        try:
            validate_mi_or_raise("de la")
        except DataValueError:
            pass
        else:
            self.fail("Expected DataValueError")

    def test_validate_mi_or_raise2(self):
        try:
            validate_mi_or_raise("N")
        except DataValueError:
            pass
        else:
            self.fail("Expected DataValueError")

    def test_validate_mi_or_raise3(self):
        try:
            validate_mi_or_raise("n")
        except DataValueError:
            pass
        else:
            self.fail("Expected DataValueError")

if __name__ == '__main__':
    unittest.main()
