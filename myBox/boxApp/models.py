from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django.contrib.postgres.fields import ArrayField
from django.db import models
import datetime
from django.utils.timezone import now


class UserManager(BaseUserManager):
    def create_user(self, email, password=None, is_active=True, is_staff=False, is_admin=False):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('Users must have an email address')
        if not password:
            raise ValueError('Users must have a password')
        user = self.model(
            email=self.normalize_email(email),
        )

        user.set_password(password)
        user.staff = is_staff
        user.admin = is_admin
        user.active = is_active
        user.save(using=self._db)
        return user

    def create_staffeuser(self, email, password=None):
        """
        Creates and saves a Athlete user with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
            is_staff = True
        )
        user.staff = True
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password):
        """
        Creates and saves a superuser with the given email and password.
        """
        user = self.create_user(
            email,
            password=password,
            is_admin = True,
            is_staff = True
        )
        user.staff = True
        user.admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    active = models.BooleanField(default=True)
    staff = models.BooleanField(default=False) 
    admin = models.BooleanField(default=False) 

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def get_full_name(self):
        # The user is identified by their email address
        return self.email

    def get_short_name(self):
        # The user is identified by their email address
        return self.email

    def __str__(self):              # __unicode__ on Python 2
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def is_active(self):
        "Is the user active?"
        return self.active


class Athlete(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,)
    # Extra Data
    iban = models.CharField(max_length=50)

    def __str__(self):
        return self.user.email


class Coach(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,)
    # Extra Data

    def __str__(self):
        return self.user.email


class Training(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    athletes_limit = models.IntegerField(default=30)
    bookings = models.IntegerField(default=0)
    text = models.TextField(u'Textual Notes', help_text=u'Textual Notes', blank=True, null=True)
    date = models.DateField(u'Day of the event', help_text=u'Day of the event', null=True)
    start_time = models.TimeField(u'Starting time', help_text=u'Starting time', null=True)
    end_time = models.TimeField(u'Final time', help_text=u'Final time', null=True)
    # Attribute to save Exercise ids
    ex_list = ArrayField(models.IntegerField(), null=True)
    # Think about saving the reps and time of each exercise
    date_published = models.DateTimeField(default=now, editable=False)

    def get_exercises(self):
        """Returns list with all the exercise objects associated to the training"""
        exercises_list = []
        for i in self.ex_list:
            ex = Exercise.objects.get(id=self.ex_list[i])
            exercises_list.extend(ex)
        return exercises_list

    def get_exercise_by_position(self, position):

        """Returns exercise by position starts at 0"""
        try:
            if 0 <= position <= len(self.ex_list):
                id = self.ex_list[position]
                exercise = Exercise.objects.get(id=id)
                return exercise
            else:
                raise ValueError
        except ValueError:
            print('Position does no correspond with exercises length')

    def remove_exercise_by_id(self, id):
        """Remove Exercise in training by id"""
        try:
            ex = Training.objects.get(id=id)
            if ex is not None:
                self.ex_list.remove(id)
                self.save()
            else:
                print('valor erroneo')
                raise ValueError
        except ValueError:
            print('Position does no correspond with exercises length')

    def add_exercise(self, id):
        if Exercise.objects.get(id=id) is not None:
            self.ex_list.append(id)
            self.save()
        else:
            print("The id doesn't correspond with any Exercise")

    def move_exercise(self, id, position):
        if Exercise.objects.get(id=id) is not None:

            self.ex_list.remove(id)
            if 0 <= position <= len(self.ex_list):

                self.ex_list.insert(id, position)
                self.save()

            else:
                print('Position does no correspond with exercises length')
        else:
            print("The id doesn't correspond with any Exercise")


# """
#     def book_training(self,user):
#     """Creates a booking for a user in the corresponding tra    """
#         if user.class_tickets>0 and self.bookings<self.athletes_limit:
#             user.class_tickets=user.class_tickets+1
#             self.bookings=self.bookings+1
#             booking=Booking(user,self)
#             booking.save()
#         else:
#             print('Not enough tickets or space in the class')
# """


class Exercise(models.Model):
    name = models.CharField(max_length=50)
    text = models.TextField(max_length=500, blank=True)
    difficulty = models.CharField(max_length=100)
    img_url = models.CharField(max_length=100)
    video_url = models.CharField(max_length=100)
    date_published = models.DateTimeField('Date published', null=True)


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    training = models.ForeignKey(Training, on_delete=models.SET_NULL, null=True)
    user_tickets = models.IntegerField()
    training_space = models.IntegerField()
    date_published = models.DateTimeField(default=now, editable=False)

    def remove_booking(self):

        Booking.objects.remove(id=self.id)
