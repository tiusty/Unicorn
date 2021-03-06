# Django Imports
from django.db import models
from django.utils import timezone

# Import constants
from .constants import ZIP_CODE_TIMEDELTA_VALUE


class CommuteType(models.Model):
    """
    Class stores all the different commute types
    This generates a choice field in the survey
    If another commute type gets added, it should get added to the COMMUTE_TYPES field
    """

    WORK_FROM_HOME = 'wh'
    DRIVING = 'dr'
    TRANSIT = 'tr'
    WALKING = 'wk'
    BICYCLING = 'bk'

    COMMUTE_TYPES = (
        (WORK_FROM_HOME, 'Work From Home'),
        (DRIVING, 'Driving'),
        (TRANSIT, 'Transit'),
        (WALKING, 'Walking'),
        (BICYCLING, 'Biking'),
    )

    commute_type = models.CharField(
        unique=True,
        choices=COMMUTE_TYPES,
        max_length=2,
    )

    def __str__(self):
        return self.get_commute_type_display()


class ZipCodeBase(models.Model):
    """
    This is the base zip-code which is what all the child zip_codes are computed relative too.
    """
    zip_code = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.zip_code


class ZipCodeChild(models.Model):
    """
    This is the child zip-code which computes the time and distance from this child zip_code to the
    base zip-code. Each base zip-code will have a bunch of child zip-codes. For each base zip-code, there
    can be a child zip-code for each commute type.
    """
    zip_code = models.CharField(max_length=20)
    base_zip_code = models.ForeignKey('ZipCodeBase', on_delete=models.CASCADE)
    commute_time_seconds = models.IntegerField(default=-1)
    commute_distance_meters = models.IntegerField(default=-1)
    last_date_updated = models.DateField(default=timezone.now)
    commute_type = models.ForeignKey('CommuteType', on_delete=models.PROTECT)

    def __str__(self):
        return self.zip_code

    @property
    def commute_time_minutes(self):
        """
        Returns the commute time in seconds
        :return: (int) -> The commute time in seconds
        """
        return self.commute_time_seconds / 60

    @property
    def commute_distance_miles(self):
        """
        Returns the commute distance in meters
        :return: (int) -> The commute distance in meters
        """
        return self.commute_distance_meters * 0.000621371

    def zip_code_cache_still_valid(self):
        """
        This function tests whether or not the zip code should be recalculated.
        The time is set by the value in constants.py
        :return: (Boolean) -> True: The cache is still valid
                              False: The cache is no longer valid
        """
        return self.zip_code_cache_valid_check(self.last_date_updated)

    @staticmethod
    def zip_code_cache_valid_check(last_date_updated):
        """
        This function tests whether or not the zip code should be recalculated.
        The time is set by the value in constants.py.
        :param: (Datetime) -> The date time to test to see if that time is still valid
        :return: (Boolean) -> True: The cache is still valid
                              False: The cache is no longer valid
        """
        if timezone.now().date() > last_date_updated + timezone.timedelta(days=ZIP_CODE_TIMEDELTA_VALUE):
            return False
        else:
            return True
