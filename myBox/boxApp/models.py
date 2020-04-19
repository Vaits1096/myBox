from django.db import models

# Create your models here.

class Training(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    text = models.TextField(max_length=500)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    date_published = models.DateField('Date published')
    exerid_list = []

    def __init__(self, id, name, typeid, text, time, img_url, exerid_list=None):
        self.id = id
        self.name = name
        self.typeid = typeid
        self.text = text
        self.time = time
        self.img_url = img_url
        self.date_published = date.today()
        self.exerid_list = exerid_list

    def get_exercises(self):
        exer_list = []
        for i in self.exerid_list:
            ex = Exercise.get_exercise_by_id(i)
            exer_list.extend(ex)
        return exer_list


class Exercise(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    text = models.TextField(max_length=500)
    difficulty = models.CharField(max_length=100)
    img_url = models.CharField(max_length=100)
    video_url = models.CharField(max_length=100)
    date_published = models.DateField('Date published')

    def __init__(self, id, name, text, difficulty, img_url=None, video_url=None, date_published=None):
        self.id = id
        self.name = name
        self.text = text
        self.difficulty = difficulty
        self.img_url = img_url
        self.video_url = video_url
        self.date_published = date_published

    def get_exercise_by_id(self, id):
        return Exercise.objects.filter(id=id)

