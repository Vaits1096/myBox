from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
from django.db import models
import datetime

from django.utils import timezone
from django.utils.timezone import now


# Create your models here.

class Training(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    athletes_limit = models.IntegerField(default=30)
    bookings = models.IntegerField(default=0)
    text = models.TextField(u'Textual Notes', help_text=u'Textual Notes', blank=True, null=True)
    date = models.DateField(u'Day of the event', help_text=u'Day of the event', null=True)
    start_time = models.TimeField(u'Starting time', help_text=u'Starting time', null=True)
    end_time = models.TimeField(u'Final time', help_text=u'Final time', null=True)
    #Add trainer foreign key
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
    text = models.CharField(max_length=500, blank=True)
    difficulty = models.CharField(max_length=100)
    img = models.ImageField(upload_to='images/',blank=True)
    video_url = models.CharField(max_length=100,blank=True)
    #add trainer who added it
    #last_modified = models.DateTimeField('Date modified', default=timezone.now)
    date_published = models.DateTimeField('Date published', default=timezone.now)

    def __str__(self):
        return self.name

class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    training = models.ForeignKey(Training, on_delete=models.SET_NULL, null=True)
    user_tickets = models.IntegerField()
    training_space = models.IntegerField()
    date_published = models.DateTimeField(default=now, editable=False)

    def remove_booking(self):

        Booking.objects.remove(id=self.id)
