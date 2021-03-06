from django.test import TestCase

# Import Cocoon Modules
from cocoon.userAuth.constants import BROKER_CREATION_KEY
from cocoon.userAuth.forms import ApartmentHunterSignupForm, BrokerSignupForm
from ..models import MyUser


class TestApartmentHunterSignupForm(TestCase):

    def tests_form_valid(self):
        """
        Tests that given the correct info the form will validate
        """
        # Arrange
        first_name = 'Alex'
        last_name = 'Agudelo'
        username = 'email@text.com'
        password1 = 'sometestPassword'
        password2 = 'sometestPassword'

        # Create form data
        form_data = {
            'first_name': first_name,
            'last_name': last_name,
            'email': username,
            'password1': password1,
            'password2': password2,
        }

        # Act
        form = ApartmentHunterSignupForm(data=form_data)

        # Assert
        self.assertTrue(form.is_valid())

    def test_form_not_matching_passwords(self):
        """
        Tests that given non-matching passwords, the form will not validate
        :return:
        """
        # Arrange
        first_name = 'Alex'
        last_name = 'Agudelo'
        username = 'email@text.com'
        password1 = 'sometestPassword'
        password2 = 'sometestPassword1'

        # Create form data
        form_data = {
            'first_name': first_name,
            'last_name': last_name,
            'email': username,
            'password1': password1,
            'password2': password2,
        }

        # Act
        form = ApartmentHunterSignupForm(data=form_data)

        # Assert
        self.assertFalse(form.is_valid())
        self.assertEqual({'password2': ["The two password fields didn't match."]}, form.errors)

    def test_form_email_not_valid(self):
        """
        Tests that if the email field is not a valid email, the form will not validate
        """
        # Arrange
        first_name = 'Alex'
        last_name = 'Agudelo'
        username = 'email'
        password1 = 'sometestPassword'
        password2 = 'sometestPassword'

        # Create form data
        form_data = {
            'first_name': first_name,
            'last_name': last_name,
            'email': username,
            'password1': password1,
            'password2': password2,
        }

        # Act
        form = ApartmentHunterSignupForm(data=form_data)

        # Assert
        self.assertFalse(form.is_valid())
        self.assertEqual({'email': ['Enter a valid email address.']}, form.errors)


class TTestApartmentHunterSignupForm(TestCase):

    def tests_form_valid(self):
        """
        Tests that given the correct info the form will validate
        """
        # Arrange
        first_name = 'Alex'
        last_name = 'Agudelo'
        username = 'email@text.com'
        password1 = 'sometestPassword'
        password2 = 'sometestPassword'
        creation_key = BROKER_CREATION_KEY

        # Create form data
        form_data = {
            'first_name': first_name,
            'last_name': last_name,
            'email': username,
            'password1': password1,
            'password2': password2,
            'creation_key': creation_key
        }

        # Act
        form = BrokerSignupForm(data=form_data)

        # Assert
        self.assertTrue(form.is_valid())

    def test_form_wrong_key(self):
        """
        Tests thta given the wrong key the form doesn't validate
        """
        # Arrange
        first_name = 'Alex'
        last_name = 'Agudelo'
        username = 'email@text.com'
        password1 = 'sometestPassword'
        password2 = 'sometestPassword'
        creation_key = 'some_random_key'

        # Create form data
        form_data = {
            'first_name': first_name,
            'last_name': last_name,
            'email': username,
            'password1': password1,
            'password2': password2,
            'creation_key': creation_key
        }

        # Act
        form = BrokerSignupForm(data=form_data)

        # Assert
        self.assertFalse(form.is_valid())
        self.assertEqual({'creation_key': ['Creation Key invaild']}, form.errors)

    def test_form_not_matching_passwords(self):
        """
        Tests that given non-matching passwords, the form will not validate
        :return:
        """
        # Arrange
        first_name = 'Alex'
        last_name = 'Agudelo'
        username = 'email@text.com'
        password1 = 'sometestPassword'
        password2 = 'sometestPassword1'
        creation_key = BROKER_CREATION_KEY

        # Create form data
        form_data = {
            'first_name': first_name,
            'last_name': last_name,
            'email': username,
            'password1': password1,
            'password2': password2,
            'creation_key': creation_key
        }

        # Act
        form = BrokerSignupForm(data=form_data)

        # Assert
        self.assertFalse(form.is_valid())
        self.assertEqual({'password2': ["The two password fields didn't match."]}, form.errors)

    def test_form_email_not_valid(self):
        """
        Tests that if the email field is not a valid email, the form will not validate
        """
        # Arrange
        first_name = 'Alex'
        last_name = 'Agudelo'
        username = 'email'
        password1 = 'sometestPassword'
        password2 = 'sometestPassword'
        creation_key = BROKER_CREATION_KEY

        # Create form data
        form_data = {
            'first_name': first_name,
            'last_name': last_name,
            'email': username,
            'password1': password1,
            'password2': password2,
            'creation_key': creation_key
        }

        # Act
        form = BrokerSignupForm(data=form_data)

        # Assert
        self.assertFalse(form.is_valid())
        self.assertEqual({'email': ['Enter a valid email address.']}, form.errors)

    def tests_form_valid_agent_referral(self):
        """
        Tests that if the agent referral is filled out with an agents url then the form is valid
        """
        # Arrange
        agent = MyUser.objects.create(is_broker=True)
        first_name = 'Alex'
        last_name = 'Agudelo'
        username = 'email@text.com'
        password1 = 'sometestPassword'
        password2 = 'sometestPassword'

        # Create form data
        form_data = {
            'first_name': first_name,
            'last_name': last_name,
            'email': username,
            'password1': password1,
            'password2': password2,
            'agent_referral': agent.userProfile.url,
        }

        # Act
        form = ApartmentHunterSignupForm(data=form_data)

        # Assert
        self.assertTrue(form.is_valid())

    def tests_form_not_valid_agent_referral_if_the_url_is_not_for_a_broker_account(self):
        """
        Tests that if the user puts down a user account url that is not a broker,
            then it does not validate
        """
        # Arrange
        # set agent to is_broker=False to make not a broker account
        agent = MyUser.objects.create(is_broker=False)
        first_name = 'Alex'
        last_name = 'Agudelo'
        username = 'email@text.com'
        password1 = 'sometestPassword'
        password2 = 'sometestPassword'

        # Create form data
        form_data = {
            'first_name': first_name,
            'last_name': last_name,
            'email': username,
            'password1': password1,
            'password2': password2,
            'agent_referral': agent.userProfile.url,
        }

        # Act
        form = ApartmentHunterSignupForm(data=form_data)

        # Assert
        self.assertFalse(form.is_valid())

    def tests_form_not_valid_agent_referral(self):
        """
        Tests if the agent referral is filled out with a url that is not associated with
            an agent then it isn't valid
        """
        # Arrange
        agent = MyUser.objects.create(is_broker=True)
        first_name = 'Alex'
        last_name = 'Agudelo'
        username = 'email@text.com'
        password1 = 'sometestPassword'
        password2 = 'sometestPassword'

        # Create form data
        form_data = {
            'first_name': first_name,
            'last_name': last_name,
            'email': username,
            'password1': password1,
            'password2': password2,
            'agent_referral': agent.userProfile.url + '12',
        }

        # Act
        form = ApartmentHunterSignupForm(data=form_data)

        # Assert
        self.assertFalse(form.is_valid())

    def tests_form_agent_referral_no_agents(self):
        """
        Tests that if there are no agents that exist and the user puts an agent referal then
            it will fail to be valid
        """
        # Arrange
        first_name = 'Alex'
        last_name = 'Agudelo'
        username = 'email@text.com'
        password1 = 'sometestPassword'
        password2 = 'sometestPassword'

        # Create form data
        form_data = {
            'first_name': first_name,
            'last_name': last_name,
            'email': username,
            'password1': password1,
            'password2': password2,
            'agent_referral': '23',
        }

        # Act
        form = ApartmentHunterSignupForm(data=form_data)

        # Assert
        self.assertFalse(form.is_valid())

    def tests_form_set_agent_referral(self):
        """
        Tests that if the agent referral is filled out correctly then the account is saved
            with that agent referral
        """
        # Arrange
        agent = MyUser.objects.create(is_broker=True)
        first_name = 'Alex'
        last_name = 'Agudelo'
        username = 'email@text.com'
        password1 = 'sometestPassword'
        password2 = 'sometestPassword'

        # Create form data
        form_data = {
            'first_name': first_name,
            'last_name': last_name,
            'email': username,
            'password1': password1,
            'password2': password2,
            'agent_referral': agent.userProfile.url,
        }

        # Act
        form = ApartmentHunterSignupForm(data=form_data)
        form.save()

        # Assert
        if form.is_valid():
            form.save()

            # Assert
            client = MyUser.objects.get(first_name=first_name)
            self.assertEqual(client.userProfile.referred_agent.id, agent.id)
        else:
            self.assertFalse(True, "Form failed to validate")

    def tests_form_do_not_set_agent_referral(self):
        """
        Tests that if the agent referral is not set, then the client account is saved
            with an agent referral
        """
        # Arrange
        agent = MyUser.objects.create(is_broker=True)
        first_name = 'Alex'
        last_name = 'Agudelo'
        username = 'email@text.com'
        password1 = 'sometestPassword'
        password2 = 'sometestPassword'

        # Create form data
        form_data = {
            'first_name': first_name,
            'last_name': last_name,
            'email': username,
            'password1': password1,
            'password2': password2,
        }

        # Act
        form = ApartmentHunterSignupForm(data=form_data)

        # Assert
        if form.is_valid():
            form.save()

            # Assert
            client = MyUser.objects.get(first_name=first_name)
            self.assertEqual(client.userProfile.referred_agent, None)
        else:
            self.assertFalse(True, "Form failed to validate")
