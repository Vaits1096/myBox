from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.urls import reverse
import datetime
from accounts.models import User
from django.utils import timezone
from django.utils.timezone import now


class Box(models.Model):
    name            = models.CharField(max_length = 50)
    location        = models.CharField(max_length = 50)

    def get_item_list(self, obj):
        all_item = obj.objects.all()
        item_list = []
        for i in all_item:
            if i.box.id == self.id:
                item_list.extend(i)
        return item_list

    def get_coach_list(self):
        return get_item_list(self, Coach)

    def get_athlete_list(self):
        return get_item_list(self, Athlete)

    def get_training_list(self):
        return get_item_list(self, Training)

    def get_exercise_list(self):
        return get_item_list(self, Exercise)

    def __str__(self):
        return self.name


class Coach(models.Model):
    user        = models.ForeignKey(User, on_delete=models.CASCADE)
    box         = models.ForeignKey(Box, on_delete = models.CASCADE)
    user_name   = models.CharField(max_length=50)
    name        = models.CharField(max_length=50)
    last_name   = models.CharField(max_length=50)
    birthdate   = models.DateField(default=datetime.date.today, auto_now=False, auto_now_add=False)


class Athlete(models.Model):
    user        = models.OneToOneField(User, on_delete=models.CASCADE, null = True)
    box         = models.ForeignKey(Box, on_delete = models.CASCADE)
    coach       = models.ForeignKey(Coach, on_delete = models.CASCADE, null = True, default=None)
    user_name   = models.CharField(max_length=50)
    name        = models.CharField(max_length=50)
    last_name   = models.CharField(max_length=50)
    birthdate   = models.DateField(default=datetime.date.today, auto_now=False, auto_now_add=False)

    def get_absolute_url(self):
        return reverse("athletes:athlete_detail", kwargs={"id": self.id})


class Token(models.Model):
    athlete     = models.ForeignKey(Athlete, on_delete = models.CASCADE)
    token       = models.CharField(max_length=70)


class Training(models.Model):
    box             = models.ForeignKey(Box, on_delete = models.CASCADE)
    name            = models.CharField(max_length = 50)
    type            = models.CharField(max_length = 50)
    athletes_limit  = models.IntegerField(default = 30)
    bookings        = models.IntegerField(default = 0)
    text            = models.TextField(u'Textual Notes', help_text=u'Textual Notes', blank=True, null=True)
    date            = models.DateField(u'Day of the event', help_text=u'Day of the event', null=True)
    start_time      = models.TimeField(u'Starting time', help_text=u'Starting time', null=True)
    end_time        = models.TimeField(u'Final time', help_text=u'Final time', null=True)
    #Add trainer foreign key
    # Attribute to save Exercise ids
    ex_list         = ArrayField(models.IntegerField(), null = True)
    # Think about saving the reps and time of each exercise
    date_published  = models.DateTimeField(default = now, editable = False)

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


class Exercise(models.Model):
    box         = models.ForeignKey(Box, on_delete = models.CASCADE)
    name        = models.CharField(max_length = 50)
    text        = models.CharField(max_length = 500, blank = True)
    difficulty  = models.CharField(max_length = 100)
    img         = models.ImageField(upload_to = 'images/', blank = True)
    video_url   = models.CharField(max_length = 100, blank = True)
    #add trainer who added it
    #last_modified = models.DateTimeField('Date modified', default=timezone.now)
    date_published = models.DateTimeField('Date published', default=timezone.now)

    def __str__(self):
        return self.name

class Booking(models.Model):
    box             = models.ForeignKey(Box, on_delete = models.CASCADE)
    user            = models.ForeignKey(User, on_delete = models.SET_NULL, null=True)
    training        = models.ForeignKey(Training, on_delete = models.SET_NULL, null=True)
    user_tickets    = models.IntegerField()
    training_space  = models.IntegerField()
    date_published  = models.DateTimeField(default=now, editable = False)

    def remove_booking(self):
        Booking.objects.remove(id=self.id)
