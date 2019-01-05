# Django modules
from django import forms
from django.forms import ModelForm
from django.utils.text import slugify

# Survey models
from cocoon.survey.models import RentingSurveyModel, HomeInformationModel, CommuteInformationModel, \
    PriceInformationModel, ExteriorAmenitiesModel, InteriorAmenitiesModel, DestinationsModel, TenantModel, \
    TenantPersonalInformationModel
from cocoon.houseDatabase.models import HomeTypeModel
from cocoon.commutes.models import CommuteType

# Python global configurations
from config.settings.Global_Config import MAX_TEXT_INPUT_LENGTH, MAX_NUM_BEDROOMS, DEFAULT_RENT_SURVEY_NAME, \
    WEIGHT_QUESTION_MAX, MAX_NUM_BATHROOMS, HYBRID_WEIGHT_CHOICES
from django.forms.models import inlineformset_factory

# import constants
from cocoon.survey.constants import MAX_TENANTS_FOR_ONE_SURVEY


class HomeInformationForm(ModelForm):
    num_bedrooms = forms.ChoiceField(
        choices=[(x, x) for x in range(0, MAX_NUM_BEDROOMS)],
        label="Number of Bedrooms",
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )

    max_bathrooms = forms.IntegerField(
        widget=forms.HiddenInput(
            attrs={
                'class': 'form-control',
            }),
    )

    min_bathrooms = forms.IntegerField(
        widget=forms.HiddenInput(
            attrs={
                'class': 'form-control',
            }),
    )

    wants_laundry_nearby = forms.BooleanField(
        widget=forms.HiddenInput(
            attrs={
                'class': 'form-control',
            }),
    )

    home_type = forms.ModelMultipleChoiceField(
        widget=forms.SelectMultiple(
            attrs={
                'class': 'form-control',
            }),
        queryset=HomeTypeModel.objects.all()
    )

    def is_valid(self):
        valid = super(HomeInformationForm, self).is_valid()

        if not valid:
            return valid

        # Need to make a copy because otherwise when an error is added, that field
        # is removed from the cleaned_data, then any subsequent checks of that field
        # will cause a key error
        current_form = self.cleaned_data.copy()

        if int(current_form['num_bedrooms']) < 0:
            self.add_error('num_bedrooms', "There can't be less than 1 bedroom")
            valid = False

        # Make sure the bedrooms are not more than the max allowed
        if int(current_form['num_bedrooms']) > MAX_NUM_BEDROOMS:
            self.add_error('num_bedrooms', "There can't be more than " + str(MAX_NUM_BEDROOMS))
            valid = False

        # make sure that the max number of bathrooms is not greater than the max specified
        if current_form['max_bathrooms'] > MAX_NUM_BATHROOMS:
            self.add_error('max_bathrooms', "You can't have more bathrooms than " + str(MAX_NUM_BATHROOMS))
            valid = False

        if current_form['min_bathrooms'] < 0:
            self.add_error('min_bathrooms', "You can't have less than 0 bathrooms")
            valid = False

        return valid

    class Meta:
        model = HomeInformationModel
        fields = '__all__'


class PriceInformationForm(ModelForm):

    max_price = forms.IntegerField(
        widget=forms.HiddenInput(
            attrs={
                'class': 'form-control',
            }),
    )

    desired_price = forms.IntegerField(
        widget=forms.HiddenInput(
            attrs={
                'class': 'form-control',
            }),
    )

    price_weight = forms.ChoiceField(
        choices=[(x, x) for x in range(0, WEIGHT_QUESTION_MAX)],
        label="Price Weight",
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }),
    )

    class Meta:
        model = PriceInformationModel
        fields = '__all__'


class ExteriorAmenitiesForm(ModelForm):
    """
    Class stores all the form fields for the BuildingExteriorAmenitiesModel Model
    """
    parking_spot = forms.ChoiceField(
        choices=HYBRID_WEIGHT_CHOICES,
        initial=0,
        label="Parking Spot",
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }
        )
    )

    wants_laundry_in_building = forms.BooleanField(
        widget=forms.HiddenInput(
            attrs={
                'class': 'form-control',
            }),
    )

    number_of_cars = forms.IntegerField(
        widget=forms.HiddenInput(
            attrs={
                'class': 'form-control',
            }),
    )

    wants_patio = forms.BooleanField(
        widget=forms.HiddenInput(
            attrs={
                'class': 'form-control',
            }),
    )

    patio_weight = forms.IntegerField(
        widget=forms.HiddenInput(
            attrs={
                'class': 'form-control',
            }),
    )

    wants_pool = forms.BooleanField(
        widget=forms.HiddenInput(
            attrs={
                'class': 'form-control',
            }),
    )

    pool_weight = forms.IntegerField(
        widget=forms.HiddenInput(
            attrs={
                'class': 'form-control',
            }),
    )

    wants_gym = forms.BooleanField(
        widget=forms.HiddenInput(
            attrs={
                'class': 'form-control',
            }),
    )

    gym_weight = forms.IntegerField(
        widget=forms.HiddenInput(
            attrs={
                'class': 'form-control',
            }),
    )

    wants_storage = forms.BooleanField(
        widget=forms.HiddenInput(
            attrs={
                'class': 'form-control',
            }),
    )

    storage_weight = forms.IntegerField(
        widget=forms.HiddenInput(
            attrs={
                'class': 'form-control',
            }),
    )

    class Meta:
        model = ExteriorAmenitiesModel
        fields = ["parking_spot", 'wants_laundry_in_building', 'number_of_cars',
                  'wants_patio', 'patio_weight', 'wants_pool', 'pool_weight',
                  'wants_gym', 'gym_weight', 'wants_storage', 'storage_weight']

class InteriorAmenitiesForm(ModelForm):
    """
    Class stores all the form fields for the BuildingInteriorAmenitiesModel Model
    """
    wants_laundry_in_unit = forms.BooleanField(
        widget=forms.HiddenInput(
            attrs={
                'class': 'form-control',
            }),
    )

    wants_furnished = forms.BooleanField(
        widget=forms.HiddenInput(
            attrs={
                'class': 'form-control',
            }),
    )

    furnished_weight = forms.IntegerField(
        widget=forms.HiddenInput(
            attrs={
                'class': 'form-control',
            }),
    )

    wants_dogs = forms.BooleanField(
        widget=forms.HiddenInput(
            attrs={
                'class': 'form-control',
            }),
    )

    number_of_dogs = forms.IntegerField(
        widget=forms.HiddenInput(
            attrs={
                'class': 'form-control',
            }),
    )

    wants_cats = forms.BooleanField(
        widget=forms.HiddenInput(
            attrs={
                'class': 'form-control',
            }),
    )

    cat_weight = forms.IntegerField(
        widget=forms.HiddenInput(
            attrs={
                'class': 'form-control',
            }),
    )

    wants_hardwood_floors = forms.BooleanField(
        widget=forms.HiddenInput(
            attrs={
                'class': 'form-control',
            }),
    )

    hardwood_floors_weight = forms.IntegerField(
        widget=forms.HiddenInput(
            attrs={
                'class': 'form-control',
            }),
    )

    wants_AC = forms.BooleanField(
        widget=forms.HiddenInput(
            attrs={
                'class': 'form-control',
            }),
    )

    AC_weight = forms.IntegerField(
        widget=forms.HiddenInput(
            attrs={
                'class': 'form-control',
            }),
    )

    wants_dishwasher = forms.BooleanField(
        widget=forms.HiddenInput(
            attrs={
                'class': 'form-control',
            }),
    )

    dishwasher_weight = forms.IntegerField(
        widget=forms.HiddenInput(
            attrs={
                'class': 'form-control',
            }),
    )

    class Meta:
        model = InteriorAmenitiesModel
        fields = ["wants_laundry_in_unit", "wants_furnished", "furnished_weight", "wants_dogs", "number_of_dogs",
                  "wants_cats", "cat_weight", "wants_hardwood_floors", "hardwood_floors_weight",
                  "wants_AC", "AC_weight", "wants_dishwasher", "dishwasher_weight"]


class RentSurveyForm(ExteriorAmenitiesForm, PriceInformationForm, HomeInformationForm):
    """
    Rent Survey is the rent survey on the main survey page
    """
    number_of_tenants = forms.ChoiceField(
        choices=[(x, x) for x in range(1, MAX_TENANTS_FOR_ONE_SURVEY)],
        widget=forms.Select(
            attrs={
                'class': 'form-control',
                'onchange': 'updateNumTenants()',
            },

        ),
    )

    class Meta:
        model = RentingSurveyModel
        # Make sure to set the name later, in the survey result if they want to save the result
        fields = ["num_bedrooms", "max_bathrooms", "min_bathrooms", "home_type",
                  "max_price", "desired_price", "price_weight",
                  "parking_spot", "number_of_tenants"]


class RentSurveyFormMini(ExteriorAmenitiesForm,  PriceInformationForm,
                         HomeInformationForm):
    """
    RentSurveyFormMini is the survey that is on the survey results page and allows the user to create
    quick changes. This should be mostly a subset of the RentSurveyForm
    """

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super(RentSurveyFormMini, self).__init__(*args, **kwargs)

    name = forms.CharField(
        label="Survey Name",
        initial=DEFAULT_RENT_SURVEY_NAME,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Enter the name of the survey',
            }),
        max_length=MAX_TEXT_INPUT_LENGTH,
    )

    def is_valid(self):
        valid = super(RentSurveyFormMini, self).is_valid()

        if not valid:
            return valid

        # Need to make a copy because otherwise when an error is added, that field
        # is removed from the cleaned_data, then any subsequent checks of that field
        # will cause a key error
        current_form = self.cleaned_data.copy()

        # Since slugs need to be unique and the survey name generates the slug, make sure that the new slug
        #   will not conflict with a current survey. If it does, force them to choose a new name.
        if 'name' in self.changed_data:
            if self.user.userProfile.rentingsurveymodel_set.filter(url=slugify(current_form['name'])).exists():
                self.add_error('name', "You already have a very similar name, please choose a more unique name")
                valid = False

        return valid

    class Meta:
        model = RentingSurveyModel
        fields = ["num_bedrooms", "max_bathrooms", "min_bathrooms", "home_type",
                  "max_price", "desired_price", "price_weight",
                  "parking_spot", "name"]


class DestinationForm(ModelForm):
    street_address = forms.CharField(
        required=False,
        label="Destination",
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Street Address',
                'readonly': 'readonly',
            }),
        max_length=MAX_TEXT_INPUT_LENGTH,
    )

    city = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'City',
                'readonly': 'readonly',
            }),
        max_length=MAX_TEXT_INPUT_LENGTH,
    )

    state = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'State',
                'readonly': 'readonly',
            }),
        max_length=MAX_TEXT_INPUT_LENGTH,
    )

    zip_code = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Zip Code',
                'readonly': 'readonly',
            }),
        max_length=MAX_TEXT_INPUT_LENGTH,
    )

    class Meta:
        model = DestinationsModel
        fields = '__all__'


class CommuteInformationForm(DestinationForm):

    max_commute = forms.IntegerField(
        required=False,
        widget=forms.HiddenInput(
            attrs={
                'class': 'form-control',
            }),
    )

    min_commute = forms.IntegerField(
        required=False,
        widget=forms.HiddenInput(
            attrs={
                'class': 'form-control',
            }),
    )

    commute_weight = forms.ChoiceField(
        required=False,
        choices=[(x, x) for x in range(0, WEIGHT_QUESTION_MAX)],
        label="Commute Weight",
        widget=forms.Select(
            attrs={
                'class': 'form-control',
            }),
    )

    commute_type = forms.ModelChoiceField(
        required=True,
        queryset=CommuteType.objects.all(),
        label="Commute Type",
        widget=forms.Select(
            attrs={
                'class': 'form-control'
            }
        ),
    )

    traffic_option = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Consider Traffic?',
            }),
    )

    def is_valid(self):
        valid = super().is_valid()

        if not valid:
            return valid

        # Need to make a copy because otherwise when an error is added, that field
        # is removed from the cleaned_data, then any subsequent checks of that field
        # will cause a key error
        current_form = self.cleaned_data.copy()

        if 'commute_type' in current_form:

            # only when the commute type is not work from home are these fields needed
            if current_form['commute_type'] != CommuteType.objects.get_or_create(commute_type=CommuteType.WORK_FROM_HOME)[0]:

                if not current_form['street_address']:
                    self.add_error('street_address', "Street Address Required")
                    valid = False

                if not current_form['city']:
                    self.add_error('city', "City Required")
                    valid = False

                if not current_form['state']:
                    self.add_error('state', "State required")
                    valid = False

                if not current_form['zip_code']:
                    self.add_error('zip_code', "Zip Code Required")
                    valid = False

                if not current_form['commute_weight']:
                    self.add_error('commute_weight', "Commute weight needed")
                    valid = False

                if current_form['max_commute'] is not None:
                    if int(current_form['max_commute']) < 0:
                        self.add_error('max_commute', "Max Commute needs to be above 0")
                        valid = False
                else:
                    self.add_error('max_commute', "Max Commute Needed")
                    valid = False

                if current_form['min_commute'] is not None:
                    if int(current_form['min_commute']) < 0:
                        self.add_error('min_commute', "Min commute needs to be above 0")
                        valid = False

                if current_form['min_commute'] is not None and current_form['max_commute'] is not None:
                    if int(current_form['min_commute']) > int(current_form['max_commute']):
                        self.add_error('max_commute', "Max commute needs to be above min commute")
                        valid = False

        return valid

    class Meta:
        model = CommuteInformationModel
        fields = '__all__'


class TenantPersonalInformationForm(ModelForm):
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'First Name',
            }),
        max_length=MAX_TEXT_INPUT_LENGTH,
    )

    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Last Name',
            }),
        max_length=MAX_TEXT_INPUT_LENGTH,
    )

    is_student = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(
            attrs={
                'class': 'form-control',
                'placeholder': 'Student?',
            }),
        )

    class Meta:
        model = TenantPersonalInformationModel
        fields = '__all__'


class TenantForm(CommuteInformationForm, TenantPersonalInformationForm):
    class Meta:
        model = TenantModel
        fields = ['first_name', 'last_name', 'is_student', 'street_address', 'city', 'state', 'zip_code', 'max_commute',
                  'min_commute', 'commute_weight', 'commute_type', 'traffic_option']


TenantFormSet = inlineformset_factory(RentingSurveyModel, TenantModel, form=TenantForm,
                                      extra=4, can_delete=False)
TenantFormSetResults = inlineformset_factory(RentingSurveyModel, TenantModel, form=TenantForm,
                                             extra=0, can_delete=False)
