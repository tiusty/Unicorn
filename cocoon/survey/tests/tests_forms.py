# Import Django Modules
from django.test import TestCase
from django.utils import timezone

# Import Survey Models and forms
from cocoon.survey.forms import RentSurveyForm, HomeInformationForm, CommuteInformationForm, PriceInformationForm, \
    ExteriorAmenitiesForm, InteriorAmenitiesForm, HouseNearbyAmenitiesForm, RentSurveyFormEdit
from cocoon.survey.models import RentingSurveyModel
from cocoon.houseDatabase.models import HomeTypeModel
from cocoon.commutes.models import CommuteType
from cocoon.userAuth.models import MyUser


class TestHomeInformationForm(TestCase):

    def setUp(self):

        # Create home type objects
        HomeTypeModel.objects.create(home_type="Apartment")
        HomeTypeModel.objects.create(home_type="Condo")
        HomeTypeModel.objects.create(home_type="Town House")
        HomeTypeModel.objects.create(home_type="House")

        # Home Information form fields
        self.move_in_date_start = timezone.now()
        self.move_in_date_end = timezone.now()
        self.num_bedrooms = 1
        self.max_num_bathrooms = 0
        self.min_num_bathrooms = 0
        self.polygon_filter_type = 0
        self.home_type = [HomeTypeModel.objects.get(home_type="Apartment")]
        self.wants_laundry_nearby = True

    def tests_home_information_form_valid(self):
        # Arrange
        form_data = {
            'move_in_date_start_survey': self.move_in_date_start,
            'move_in_date_end_survey': self.move_in_date_end,
            'num_bedrooms': self.num_bedrooms,
            'max_bathrooms': self.max_num_bathrooms,
            'min_bathrooms': self.min_num_bathrooms,
            'home_type': self.home_type,
            'wants_laundry_nearby': self.wants_laundry_nearby,
            'polygon_filter_type': self.polygon_filter_type,
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

    def tests_home_information_form_num_bedrooms_less_than_one(self):
        # Arrange
        form_data = {
            'move_in_date_start_survey': self.move_in_date_start,
            'move_in_date_end_survey': self.move_in_date_end,
            'num_bedrooms': -1,
            'max_bathrooms': self.max_num_bathrooms,
            'min_bathrooms': self.min_num_bathrooms,
            'home_type': self.home_type
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
            'num_bedrooms': self.num_bedrooms,
            'max_bathrooms': self.max_num_bathrooms,
            'min_bathrooms': -1,
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
        self.commute_weight = 1
        self.driving = CommuteType.objects.create(commute_type=CommuteType.DRIVING)
        self.bicycling = CommuteType.objects.create(commute_type=CommuteType.BICYCLING)
        self.transit = CommuteType.objects.create(commute_type=CommuteType.TRANSIT)
        self.walking = CommuteType.objects.create(commute_type=CommuteType.WALKING)
        self.work_from_home = CommuteType.objects.create(commute_type=CommuteType.WORK_FROM_HOME)

    def tests_commute_information_valid_not_work_from_home(self):
        """
        Tests that given all the required fields the commute form validates for all the
        commute types besides work from home
        """

        commute_types = [self.driving, self.transit, self.walking, self.bicycling]
        result = True

        for commute_type in commute_types:
            # Arrange
            form_data = {
                'max_commute': self.max_commute,
                'min_commute': self.min_commute,
                'commute_weight': self.commute_weight,
                'commute_type': commute_type.pk,
                'street_address': "Test Address",
                'city': 'test city',
                'state': 'test state',
                'zip_code': 'test zip_code',
            }
            commute_information_form = CommuteInformationForm(data=form_data)

            # Act
            result = commute_information_form.is_valid() and result

        # Assert
        self.assertTrue(result)

    def tests_commute_information_street_address_not_work_from_home(self):
        """
        Tests that if the commute type is not work from home then if street address is missing
            the form will not validate
        """
        commute_types = [self.driving, self.transit, self.walking, self.bicycling]
        result = True

        for commute_type in commute_types:
            # Arrange
            form_data = {
                'max_commute': self.max_commute,
                'min_commute': self.min_commute,
                'commute_weight': self.commute_weight,
                'commute_type': commute_type.pk,
                'city': 'test city',
                'state': 'test state',
                'zip_code': 'test zip_code',
            }
            commute_information_form = CommuteInformationForm(data=form_data)

            # Act
            result = commute_information_form.is_valid() and result

        # Assert
        self.assertFalse(result)

    def tests_commute_information_missing_city_not_work_from_home(self):
        """
        Tests that if the commute type is not work from home then if city is missing
            the form will not validate
        """
        commute_types = [self.driving, self.transit, self.walking, self.bicycling]
        result = True

        for commute_type in commute_types:
            # Arrange
            form_data = {
                'max_commute': self.max_commute,
                'min_commute': self.min_commute,
                'commute_weight': self.commute_weight,
                'commute_type': commute_type.pk,
                'street_address': "Test Address",
                'state': 'test state',
                'zip_code': 'test zip_code',
            }
            commute_information_form = CommuteInformationForm(data=form_data)

            # Act
            result = commute_information_form.is_valid() and result

        # Assert
        self.assertFalse(result)

    def tests_commute_information_missing_state_not_work_from_home(self):
        """
        Tests that if the commute type is not work from home then if the state is missing
            the form will not validate
        """
        commute_types = [self.driving, self.transit, self.walking, self.bicycling]
        result = True

        for commute_type in commute_types:
            # Arrange
            form_data = {
                'max_commute': self.max_commute,
                'min_commute': self.min_commute,
                'commute_weight': self.commute_weight,
                'commute_type': commute_type.pk,
                'street_address': "Test Address",
                'city': 'test city',
                'zip_code': 'test zip_code',
            }
            commute_information_form = CommuteInformationForm(data=form_data)

            # Act
            result = commute_information_form.is_valid() and result

        # Assert
        self.assertFalse(result)

    def tests_commute_information_missing_zip_code_not_work_from_home(self):
        """
        Tests that if the commute type is not work from home then if the zip_code is missing
            the form will not validate
        """
        commute_types = [self.driving, self.transit, self.walking, self.bicycling]
        result = True

        for commute_type in commute_types:
            # Arrange
            form_data = {
                'max_commute': self.max_commute,
                'min_commute': self.min_commute,
                'commute_weight': self.commute_weight,
                'commute_type': commute_type.pk,
                'street_address': "Test Address",
                'city': 'test city',
                'state': 'test state',
            }
            commute_information_form = CommuteInformationForm(data=form_data)

            # Act
            result = commute_information_form.is_valid() and result

        # Assert
        self.assertFalse(result)

    def tests_commute_information_missing_commute_weight_not_work_from_home(self):
        """
        Tests that if min_commute is missing and the commute type is not work from home then the form
            returns False
        """
        commute_types = [self.driving, self.transit, self.walking, self.bicycling]
        result = True

        for commute_type in commute_types:
            # Arrange
            form_data = {
                'max_commute': self.max_commute,
                'min_commute': self.min_commute,
                'commute_type': commute_type.pk,
                'street_address': "Test Address",
                'city': 'test city',
                'state': 'test state',
                'zip_code': 'test zip_code',
            }
            commute_information_form = CommuteInformationForm(data=form_data)

            # Act
            result = commute_information_form.is_valid() and result

        # Assert
        self.assertFalse(result)

    def tests_commute_information_missing_max_commute_not_work_from_home(self):
        """
        Tests that if max_commute is missing and the commute type is not work from home then the form
            returns False
        """
        commute_types = [self.driving, self.transit, self.walking, self.bicycling]
        result = True

        for commute_type in commute_types:
            # Arrange
            form_data = {
                'min_commute': self.min_commute,
                'commute_weight': self.commute_weight,
                'commute_type': commute_type.pk,
                'street_address': "Test Address",
                'city': 'test city',
                'state': 'test state',
                'zip_code': 'test zip_code',
            }
            commute_information_form = CommuteInformationForm(data=form_data)

            # Act
            result = commute_information_form.is_valid() and result

        # Assert
        self.assertFalse(result)

    def tests_commute_information_min_commute_less_than_zero_not_work_from_home(self):
        """
        Tests that if the min_commute is less than zero and the commute types is not work from home
            then valid is false
        """
        commute_types = [self.driving, self.transit, self.walking, self.bicycling]
        result = True

        for commute_type in commute_types:
            # Arrange
            form_data = {
                'max_commute': self.max_commute,
                'desired_commute': -1,
                'commute_weight': 1,
                'commute_type': commute_type.pk,
                'street_address': "Test Address",
                'city': 'test city',
                'state': 'test state',
                'zip_code': 'test zip_code',
            }
            commute_information_form = CommuteInformationForm(data=form_data)

            # Act
            result = commute_information_form.is_valid() and result

        # Assert
        self.assertFalse(result)

    def tests_commute_information_max_commute_less_than_zero_not_work_from_home(self):
        """
        Tests that if the max_commute is less than zero and the commute types is not work from home
            then valid is false
        """
        commute_types = [self.driving, self.transit, self.walking, self.bicycling]
        result = True

        for commute_type in commute_types:
            # Arrange
            form_data = {
                'max_commute': -1,
                'min_commute': self.min_commute,
                'commute_weight': 1,
                'commute_type': commute_type.pk,
                'street_address': "Test Address",
                'city': 'test city',
                'state': 'test state',
                'zip_code': 'test zip_code',
            }
            commute_information_form = CommuteInformationForm(data=form_data)

            # Act
            result = commute_information_form.is_valid() and result

        # Assert
        self.assertFalse(result)

    def tests_commute_information_max_commute_less_than_min_commute_not_work_from_home(self):
        """
        Tests that if the max_commute is less than min_commute and the commute types is not work from home
            then valid is false
        """
        commute_types = [self.driving, self.transit, self.walking, self.bicycling]
        result = True

        for commute_type in commute_types:
            # Arrange
            form_data = {
                'max_commute': 1,
                'desired_commute': 2,
                'commute_weight': 1,
                'commute_type': commute_type.pk,
                'street_address': "Test Address",
                'city': 'test city',
                'state': 'test state',
                'zip_code': 'test zip_code',
            }
            commute_information_form = CommuteInformationForm(data=form_data)

            # Act
            result = commute_information_form.is_valid() and result

        # Assert
        self.assertFalse(result)

    def tests_commute_information_valid_work_from_home(self):
        """
        Tests that work from home doesn't need any other fields to validate
        """

        # Arrange
        form_data = {
            'commute_type': self.work_from_home.pk,
        }
        commute_information_form = CommuteInformationForm(data=form_data)

        # Act
        result = commute_information_form.is_valid()

        # Assert
        self.assertTrue(result)


class TestPriceInformationForm(TestCase):

    def setUp(self):
        self.max_price = 0
        self.desired_price = 0
        self.price_weight = 0

    def tests_price_information_valid(self):
        # Arrange
        form_data = {
            'max_price': self.max_price,
            'desired_price': self.desired_price,
            'price_weight': self.price_weight,
        }
        price_information_form = PriceInformationForm(data=form_data)

        # Act
        result = price_information_form.is_valid()

        # Assert
        self.assertTrue(result)

    def tests_price_information_max_price_missing(self):
        # Arrange
        form_data = {
            'desired_price': self.desired_price,
            'price_weight': self.price_weight,
        }
        price_information_form = PriceInformationForm(data=form_data)

        # Act
        result = price_information_form.is_valid()

        # Assert
        self.assertFalse(result)

    def tests_price_information_desired_price_missing(self):
        # Arrange
        form_data = {
            'max_price': self.max_price,
            'price_weight': self.price_weight,
        }
        price_information_form = PriceInformationForm(data=form_data)

        # Act
        result = price_information_form.is_valid()

        # Assert
        self.assertFalse(result)

    def tests_price_information_price_weight_missing(self):
        # Arrange
        form_data = {
            'max_price': self.max_price,
            'desired_price': self.desired_price,
        }
        price_information_form = PriceInformationForm(data=form_data)

        # Act
        result = price_information_form.is_valid()

        # Assert
        self.assertFalse(result)


class TestAmenitiesForm(TestCase):

    def setUp(self):
        self.parking_spot = 0
        self.number_of_cars = 0
        self.wants_laundry_in_building = False
        self.wants_patio = False
        self.patio_weight = 0
        self.wants_pool = False
        self.pool_weight = 0
        self.wants_gym = False
        self.gym_weight = 0
        self.wants_storage = False
        self.storage_weight = 0

        self.wants_laundry_in_unit = False
        self.wants_furnished = False
        self.furnished_weight = 0
        self.wants_dogs = False
        self.number_of_dogs = 0
        self.wants_cats = False
        self.cat_weight = 0
        self.wants_hardwood_floors = False
        self.hardwood_floors_weight = 0
        self.wants_AC = False
        self.AC_weight = 0
        self.wants_dishwasher = False
        self.dishwasher_weight = 0

        self.wants_laundry_nearby = False

    def tests_exterior_amenities_valid(self):
        # Arrange
        form_data = {
            'number_of_cars': self.number_of_cars,
            'wants_laundry_in_building': self.wants_laundry_in_building,
            'wants_patio': self.wants_patio,
            'patio_weight': self.patio_weight,
            'wants_pool': self.wants_pool,
            'pool_weight': self.pool_weight,
            'wants_gym': self.wants_gym,
            'gym_weight': self.gym_weight,
            'wants_storage': self.wants_storage,
            'storage_weight': self.storage_weight
        }
        exterior_amenities_form = ExteriorAmenitiesForm(data=form_data)

        # Act
        result = exterior_amenities_form.is_valid()

        # Assert
        self.assertTrue(result)

    def tests_interior_amenities_valid(self):
        # Arrange
        form_data = {
            'parking_spot': self.parking_spot,
            "wants_laundry_in_unit": self.wants_laundry_in_unit,
            'wants_furnished': self.wants_furnished,
            'furnished_weight': self.furnished_weight,
            'wants_dogs': self.wants_dogs,
            'number_of_dogs': self.number_of_dogs,
            'wants_cats': self.wants_cats,
            'cat_weight': self.cat_weight,
            'wants_hardwood_floors': self.wants_hardwood_floors,
            'hardwood_floors_weight': self.hardwood_floors_weight,
            'wants_AC': self.wants_AC,
            'AC_weight': self.AC_weight,
            'wants_dishwasher': self.wants_dishwasher,
            'dishwasher_weight': self.dishwasher_weight
        }
        interior_amenities_form = InteriorAmenitiesForm(data=form_data)

        # Act
        result = interior_amenities_form.is_valid()

        # Assert
        self.assertTrue(result)

    def tests_nearby_amenities_valid(self):
        # Arrange
        form_data = {
            "wants_laundry_nearby": self.wants_laundry_nearby
        }
        nearby_amenities_form = HouseNearbyAmenitiesForm(data=form_data)

        # Act
        result = nearby_amenities_form.is_valid()

        # Assert
        self.assertTrue(result)


class TestRentSurveyForm(TestCase):

    def setUp(self):
        # Create home type objects
        HomeTypeModel.objects.create(home_type="Apartment")
        HomeTypeModel.objects.create(home_type="Condo")
        HomeTypeModel.objects.create(home_type="Town House")
        HomeTypeModel.objects.create(home_type="House")

        # Home Information form fields
        self.move_in_date_start = timezone.now()
        self.move_in_date_end = timezone.now()
        self.num_bedrooms = 1
        self.max_num_bathrooms = 0
        self.min_num_bathrooms = 0
        self.home_type = [HomeTypeModel.objects.get(home_type="Apartment")]
        self.number_of_tenants = 1

        self.max_commute = 0
        self.min_commute = 0
        self.commute_weight = 0
        self.commute_type = CommuteType.objects.create(commute_type=CommuteType.DRIVING)

        self.max_price = 0
        self.desired_price = 0
        self.price_weight = 0

        self.air_conditioning = 0
        self.interior_washer_dryer = 0
        self.dish_washer = 0
        self.bath = 0

        self.parking_spot = 0
        self.building_washer_dryer = 0
        self.elevator = 0
        self.handicap_access = 0
        self.pool_hot_tub = 0
        self.fitness_center = 0
        self.storage_unit = 0

        self.number_of_cars = 0
        self.wants_laundry_in_building = False
        self.wants_patio = False
        self.patio_weight = 0
        self.wants_pool = False
        self.pool_weight = 0
        self.wants_gym = False
        self.gym_weight = 0
        self.wants_storage = False
        self.storage_weight = 0

        self.wants_laundry_nearby = False


        self.number_of_destinations = 1
        self.polygon_filter_type = 0

    def tests_rent_survey_valid(self):
        # Arrange
        form_data = {
            'move_in_date_start_survey': self.move_in_date_start,
            'move_in_date_end_survey': self.move_in_date_end,
            'num_bedrooms': self.num_bedrooms,
            'max_bathrooms': self.max_num_bathrooms,
            'min_bathrooms': self.min_num_bathrooms,
            'number_of_tenants':self.number_of_tenants,
            'home_type': self.home_type,
            'max_commute': self.max_commute,
            'min_commute': self.min_commute,
            'commute_weight': self.commute_weight,
            'commute_type': self.commute_type,
            'max_price': self.max_price,
            'desired_price': self.desired_price,
            'price_weight': self.price_weight,
            'parking_spot': self.parking_spot,
            'wants_laundry_nearby': self.wants_laundry_nearby,
            'number_of_cars': self.number_of_cars,
            'wants_laundry_in_building': self.wants_laundry_in_building,
            'wants_patio': self.wants_patio,
            'patio_weight': self.patio_weight,
            'wants_pool': self.wants_pool,
            'pool_weight': self.pool_weight,
            'wants_gym': self.wants_gym,
            'gym_weight': self.gym_weight,
            'wants_storage': self.wants_storage,
            'storage_weight': self.storage_weight,
            'polygon_filter_type': self.polygon_filter_type
        }
        rent_survey_form = RentSurveyForm(data=form_data)

        # Act
        result = rent_survey_form.is_valid()
        print(rent_survey_form.errors)
        # Assert
        self.assertTrue(result)

    def tests_rent_survey_missing_home_information_data(self):
        # Arrange
        form_data = {
            'max_commute': self.max_commute,
            'min_commute': self.min_commute,
            'commute_weight': self.commute_weight,
            'commute_type': self.commute_type,
            'max_price': self.max_price,
            'desired_price': self.desired_price,
            'price_weight': self.price_weight,
            'parking_spot': self.parking_spot,
            'number_of_cars': self.number_of_cars,
            'wants_laundry_in_building': self.wants_laundry_in_building,
            'wants_patio': self.wants_patio,
            'patio_weight': self.patio_weight,
            'wants_pool': self.wants_pool,
            'pool_weight': self.pool_weight,
            'wants_gym': self.wants_gym,
            'gym_weight': self.gym_weight,
            'wants_storage': self.wants_storage,
            'storage_weight': self.storage_weight
        }
        rent_survey_form = RentSurveyForm(data=form_data)

        # Act
        result = rent_survey_form.is_valid()

        # Assert
        self.assertFalse(result)

    def tests_rent_survey_missing_price_information_data(self):
        # Arrange
        form_data = {
            'move_in_date_start_survey': self.move_in_date_start,
            'move_in_date_end_survey': self.move_in_date_end,
            'num_bedrooms': self.num_bedrooms,
            'max_bathrooms': self.max_num_bathrooms,
            'min_bathrooms': self.min_num_bathrooms,
            'home_type': self.home_type,
            'max_commute': self.max_commute,
            'min_commute': self.min_commute,
            'commute_weight': self.commute_weight,
            'commute_type': self.commute_type,
            'parking_spot': self.parking_spot,
            'number_of_cars': self.number_of_cars,
            'wants_laundry_in_building': self.wants_laundry_in_building,
            'wants_patio': self.wants_patio,
            'patio_weight': self.patio_weight,
            'wants_pool': self.wants_pool,
            'pool_weight': self.pool_weight,
            'wants_gym': self.wants_gym,
            'gym_weight': self.gym_weight,
            'wants_storage': self.wants_storage,
            'storage_weight': self.storage_weight
        }
        rent_survey_form = RentSurveyForm(data=form_data)

        # Act
        result = rent_survey_form.is_valid()

        # Assert
        self.assertFalse(result)

    def tests_rent_survey_missing_exterior_amenities_data(self):
        # Arrange
        form_data = {
            'move_in_date_start_survey': self.move_in_date_start,
            'move_in_date_end_survey': self.move_in_date_end,
            'num_bedrooms': self.num_bedrooms,
            'max_bathrooms': self.max_num_bathrooms,
            'min_bathrooms': self.min_num_bathrooms,
            'home_type': self.home_type,
            'max_commute': self.max_commute,
            'min_commute': self.min_commute,
            'commute_weight': self.commute_weight,
            'commute_type': self.commute_type,
            'max_price': self.max_price,
            'desired_price': self.desired_price,
            'price_weight': self.price_weight,
            'parking_spot': self.parking_spot,
            'number_of_cars': self.number_of_cars,
            'wants_laundry_in_building': self.wants_laundry_in_building,
            'wants_patio': self.wants_patio,
            'patio_weight': self.patio_weight,
            'wants_pool': self.wants_pool,
            'pool_weight': self.pool_weight,
            'wants_gym': self.wants_gym,
            'gym_weight': self.gym_weight,
            'wants_storage': self.wants_storage,
            'storage_weight': self.storage_weight
        }
        rent_survey_form = RentSurveyForm(data=form_data)

        # Act
        result = rent_survey_form.is_valid()

        # Assert
        self.assertFalse(result)
