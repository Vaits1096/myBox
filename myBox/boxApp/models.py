from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils.timezone import timezone
import datetime
from datetime import date


# Create your models here.

class Training(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    athletes_limit = models.IntegerField()
    bookings = models.IntegerField()
    text = models.TextField(u'Textual Notes', help_text=u'Textual Notes', blank=True, null=True)
    date = models.DateField(u'Day of the event', help_text=u'Day of the event', null=True)
    start_time = models.TimeField(u'Starting time', help_text=u'Starting time', null=True)
    end_time = models.TimeField(u'Final time', help_text=u'Final time', null=True)
    # Attribute to save Exercise ids
    ex_list = ArrayField(models.IntegerField(), null=True)
    # Think about saving the reps and time of each exercise
    date_published = models.DateTimeField(default=timezone.now, editable=False)

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
            self.ex_list.extend(id)
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
    """Object that represents the booking of an athlete in a Training"""
    user = models.ForeignKey(User, on_delete=models.SET_NULL)
    training = models.ForeignKey(Training, on_delete=models.CASCADE)
    user_tickets = models.IntegerField()
    training_limit = models.IntegerField()
    date_published = models.DateTimeField(default=datetime.now, blank=True)
