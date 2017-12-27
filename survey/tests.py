# Import Django Modules
from django.test import TestCase
from django.utils import timezone

# Import Survey Models and forms
from survey.forms import RentSurvey, HomeInformationForm, CommuteInformationForm, PriceInformationForm
from survey.models import HomeTypeModel

# Import cocoon global config values
from Unicorn.settings.Global_Config import MAX_NUM_BEDROOMS, WEIGHT_QUESTION_MAX


class TestHomeInformationForm(TestCase):

    def setUp(self):

        # Create home type objects
        HomeTypeModel.objects.create(home_type_survey="Apartment")
        HomeTypeModel.objects.create(home_type_survey="Condo")
        HomeTypeModel.objects.create(home_type_survey="Town House")
        HomeTypeModel.objects.create(home_type_survey="House")

        # Home Information form fields
        self.move_in_date_start = timezone.now()
        self.move_in_date_end = timezone.now()
        self.num_bedrooms = 1
        self.max_num_bathrooms = 0
        self.min_num_bathrooms = 0
        self.home_type_survey = [HomeTypeModel.objects.get(home_type_survey="Apartment")]

    def tests_home_information_form_valid(self):
        # Arrange
        form_data = {
            'move_in_date_start_survey': self.move_in_date_start,
            'move_in_date_end_survey': self.move_in_date_end,
            'num_bedrooms_survey': self.num_bedrooms,
            'max_bathrooms_survey': self.max_num_bathrooms,
            'min_bathrooms_survey': self.min_num_bathrooms,
            'home_type_survey': self.home_type_survey
        }
        home_information_form = HomeInformationForm(data=form_data)

        # Act
        result = home_information_form.is_valid()

        # Assert
        self.assertTrue(result)

    def tests_home_information_form_not_valid(self):
        # Arrange
        form_data = {}

        home_information_form = HomeInformationForm(data=form_data)

        # Act
        result = home_information_form.is_valid()

        # Assert
        self.assertFalse(result)

    def tests_home_information_form_move_in_date_start_missing(self):
        # Arrange
        form_data = {
            'move_in_date_end_survey': self.move_in_date_end,
            'num_bedrooms_survey': self.num_bedrooms,
            'max_bathrooms_survey': self.max_num_bathrooms,
            'min_bathrooms_survey': self.min_num_bathrooms,
            'home_type_survey': self.home_type_survey
        }
        home_information_form = HomeInformationForm(data=form_data)

        # Act
        result = home_information_form.is_valid()

        # Assert
        self.assertFalse(result)

    def tests_home_information_form_move_in_date_start_not_valid_in_past(self):
        # Arrange
        form_data = {
            'move_in_date_start_survey': timezone.now() + timezone.timedelta(days=-1),
            'move_in_date_end_survey': self.move_in_date_end,
            'num_bedrooms_survey': self.num_bedrooms,
            'max_bathrooms_survey': self.max_num_bathrooms,
            'min_bathrooms_survey': self.min_num_bathrooms,
            'home_type_survey': self.home_type_survey
        }
        home_information_form = HomeInformationForm(data=form_data)

        # Act
        result = home_information_form.is_valid()

        # Assert
        self.assertFalse(result)

    def tests_home_information_form_move_in_date_end_missing(self):
        # Arrange
        form_data = {
            'move_in_date_start_survey': self.move_in_date_start,
            'num_bedrooms_survey': self.num_bedrooms,
            'max_bathrooms_survey': self.max_num_bathrooms,
            'min_bathrooms_survey': self.min_num_bathrooms,
            'home_type_survey': self.home_type_survey
        }
        home_information_form = HomeInformationForm(data=form_data)

        # Act
        result = home_information_form.is_valid()

        # Assert
        self.assertFalse(result)

    def tests_home_information_form_move_in_date_end_before_start_date(self):
        # Arrange
        form_data = {
            'move_in_date_start_survey': self.move_in_date_start,
            'move_in_date_end_survey': timezone.now() + timezone.timedelta(days=-1),
            'num_bedrooms_survey': self.num_bedrooms,
            'max_bathrooms_survey': self.max_num_bathrooms,
            'min_bathrooms_survey': self.min_num_bathrooms,
            'home_type_survey': self.home_type_survey
        }
        home_information_form = HomeInformationForm(data=form_data)

        # Act
        result = home_information_form.is_valid()

        # Assert
        self.assertFalse(result)

    def tests_home_information_form_num_bedrooms_missing(self):
        # Arrange
        form_data = {
            'move_in_date_start_survey': self.move_in_date_start,
            'move_in_date_end_survey': self.move_in_date_end,
            'max_bathrooms_survey': self.max_num_bathrooms,
            'min_bathrooms_survey': self.min_num_bathrooms,
            'home_type_survey': self.home_type_survey
        }
        home_information_form = HomeInformationForm(data=form_data)

        # Act
        result = home_information_form.is_valid()

        # Assert
        self.assertFalse(result)

    def tests_home_information_form_num_bedrooms_less_than_one(self):
        # Arrange
        form_data = {
            'move_in_date_start_survey': self.move_in_date_start,
            'move_in_date_end_survey': self.move_in_date_end,
            'num_bedrooms_survey': 0,
            'max_bathrooms_survey': self.max_num_bathrooms,
            'min_bathrooms_survey': self.min_num_bathrooms,
            'home_type_survey': self.home_type_survey
        }
        home_information_form = HomeInformationForm(data=form_data)

        # Act
        result = home_information_form.is_valid()

        # Assert
        self.assertFalse(result)

    def tests_home_information_form_max_num_bedrooms_missing(self):
        # Arrange
        form_data = {
            'move_in_date_start_survey': self.move_in_date_start,
            'move_in_date_end_survey': self.move_in_date_end,
            'num_bedrooms_survey': self.num_bedrooms,
            'min_bathrooms_survey': self.min_num_bathrooms,
            'home_type_survey': self.home_type_survey
        }
        home_information_form = HomeInformationForm(data=form_data)

        # Act
        result = home_information_form.is_valid()

        # Assert
        self.assertFalse(result)

    def tests_home_information_form_num_bedrooms_more_than_max_num_bedrooms(self):
        # Arrange
        form_data = {
            'move_in_date_start_survey': self.move_in_date_start,
            'move_in_date_end_survey': self.move_in_date_end,
            'num_bedrooms_survey': MAX_NUM_BEDROOMS + 1,
            'max_bathrooms_survey': self.max_num_bathrooms,
            'min_bathrooms_survey': self.min_num_bathrooms,
            'home_type_survey': self.home_type_survey
        }
        home_information_form = HomeInformationForm(data=form_data)

        # Act
        result = home_information_form.is_valid()

        # Assert
        self.assertFalse(result)

    def tests_home_information_form_missing_min_num_bedrooms(self):
        # Arrange
        form_data = {
            'move_in_date_start_survey': self.move_in_date_start,
            'move_in_date_end_survey': self.move_in_date_end,
            'num_bedrooms_survey': self.num_bedrooms,
            'max_bathrooms_survey': self.max_num_bathrooms,
            'home_type_survey': self.home_type_survey
        }
        home_information_form = HomeInformationForm(data=form_data)

        # Act
        result = home_information_form.is_valid()

        # Assert
        self.assertFalse(result)

    def tests_home_information_form_min_bedrooms_less_than_zero(self):
        # Arrange
        form_data = {
            'move_in_date_start_survey': self.move_in_date_start,
            'move_in_date_end_survey': self.move_in_date_end,
            'num_bedrooms_survey': self.num_bedrooms,
            'max_bathrooms_survey': self.max_num_bathrooms,
            'min_bathrooms_survey': -1,
            'home_type_survey': self.home_type_survey
        }
        home_information_form = HomeInformationForm(data=form_data)

        # Act
        result = home_information_form.is_valid()

        # Assert
        self.assertFalse(result)

    def tests_home_information_form_home_type_missing(self):
        # Arrange
        form_data = {
            'move_in_date_start_survey': self.move_in_date_start,
            'move_in_date_end_survey': self.move_in_date_end,
            'num_bedrooms_survey': self.num_bedrooms,
            'max_bathrooms_survey': self.max_num_bathrooms,
            'min_bathrooms_survey': -1,
        }
        home_information_form = HomeInformationForm(data=form_data)

        # Act
        result = home_information_form.is_valid()

        # Assert
        self.assertFalse(result)


class TestCommuteInformationForm(TestCase):

    def setUp(self):
        self.max_commute = 0
        self.min_commute = 0
        self.commute_weight = 0
        self.commute_type = 'driving'

    def tests_commute_information_valid(self):
        # Arrange
        form_data = {
            'max_commute_survey': self.max_commute,
            'min_commute_survey': self.min_commute,
            'commute_weight_survey': self.commute_weight,
            'commute_type_survey': self.commute_type
        }
        commute_information_form = CommuteInformationForm(data=form_data)

        # Act
        result = commute_information_form.is_valid()

        # Assert
        self.assertTrue(result)

    def tests_commute_information_max_commute_missing(self):
        # Arrange
        form_data = {
            'min_commute_survey': self.min_commute,
            'commute_weight_survey': self.commute_weight,
            'commute_type_survey': self.commute_type
        }
        commute_information_form = CommuteInformationForm(data=form_data)

        # Act
        result = commute_information_form.is_valid()

        # Assert
        self.assertFalse(result)

    def tests_commute_information_min_commute_missing(self):
        # Arrange
        form_data = {
            'max_commute_survey': self.max_commute,
            'commute_weight_survey': self.commute_weight,
            'commute_type_survey': self.commute_type
        }
        commute_information_form = CommuteInformationForm(data=form_data)

        # Act
        result = commute_information_form.is_valid()

        # Assert
        self.assertFalse(result)

    def tests_commute_information_commute_weight_missing(self):
        # Arrange
        form_data = {
            'max_commute_survey': self.max_commute,
            'min_commute_survey': self.min_commute,
            'commute_type_survey': self.commute_type
        }
        commute_information_form = CommuteInformationForm(data=form_data)

        # Act
        result = commute_information_form.is_valid()

        # Assert
        self.assertFalse(result)

    def tests_commute_information_commute_weight_over_weight_question_max(self):
        # Arrange
        form_data = {
            'max_commute_survey': self.max_commute,
            'min_commute_survey': self.min_commute,
            'commute_weight_survey': WEIGHT_QUESTION_MAX + 1,
            'commute_type_survey': self.commute_type
        }
        commute_information_form = CommuteInformationForm(data=form_data)

        # Act
        result = commute_information_form.is_valid()

        # Assert
        self.assertFalse(result)

    def tests_commute_information_commute_weight_under_zero(self):
        # Arrange
        form_data = {
            'max_commute_survey': self.max_commute,
            'min_commute_survey': self.min_commute,
            'commute_weight_survey': -1,
            'commute_type_survey': self.commute_type
        }
        commute_information_form = CommuteInformationForm(data=form_data)

        # Act
        result = commute_information_form.is_valid()

        # Assert
        self.assertFalse(result)

    def tests_commute_information_commute_type_missing(self):
        # Arrange
        form_data = {
            'max_commute_survey': self.max_commute,
            'min_commute_survey': self.min_commute,
            'commute_weight_survey': -1,
        }
        commute_information_form = CommuteInformationForm(data=form_data)

        # Act
        result = commute_information_form.is_valid()

        # Assert
        self.assertFalse(result)


class TestPriceInformationForm(TestCase):

    def setUp(self):
        self.max_price = 0
        self.min_price = 0
        self.price_weight = 0

    def tests_price_information_valid(self):
        # Arrange
        form_data = {
            'max_price_survey': self.max_price,
            'min_price_survey': self.min_price,
            'price_weight_survey': self.price_weight,
        }
        price_information_form = PriceInformationForm(data=form_data)

        # Act
        result = price_information_form.is_valid()

        # Assert
        self.assertTrue(result)

    def tests_price_information_max_price_missing(self):
        # Arrange
        form_data = {
            'min_price_survey': self.min_price,
            'price_weight_survey': self.price_weight,
        }
        price_information_form = PriceInformationForm(data=form_data)

        # Act
        result = price_information_form.is_valid()

        # Assert
        self.assertFalse(result)

    def tests_price_information_min_price_missing(self):
        # Arrange
        form_data = {
            'max_price_survey': self.max_price,
            'price_weight_survey': self.price_weight,
        }
        price_information_form = PriceInformationForm(data=form_data)

        # Act
        result = price_information_form.is_valid()

        # Assert
        self.assertFalse(result)

    def tests_price_information_price_weight_missing(self):
        # Arrange
        form_data = {
            'max_price_survey': self.max_price,
            'min_price_survey': self.min_price,
        }
        price_information_form = PriceInformationForm(data=form_data)

        # Act
        result = price_information_form.is_valid()

        # Assert
        self.assertFalse(result)
