from django.db import models
import uuid
from user.models import Profile

# Create your models here.
class Project(models.Model):
    owner = models.ForeignKey(Profile, on_delete = models.CASCADE, null = True, blank = True)
    title = models.CharField(max_length = 200)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to = 'img', default = 'img/default.jpg')
    tags = models.ManyToManyField('Tag')
    demo_link = models.CharField(max_length = 2000, null=True, blank=True)
    source_link = models.CharField(max_length = 2000, null=True, blank=True)
    id = models.UUIDField(default = uuid.uuid4, editable = False, unique = True, primary_key = True)
    vote_ratio = models.IntegerField(default=0, null = True, blank = True)
    vote_total = models.IntegerField(default=0, null = True, blank = True)
    created = models.DateTimeField(auto_now_add = True)

    class Meta:
        ordering = ['-vote_ratio', '-vote_total', 'title']
    

    @property
    def reviewers(self):
        queryset = self.review_set.all().values_list('owner__id', flat=True)
        return queryset

    @property
    def getVoteCount(self):
        reviews = self.review_set.all()
        upvote = reviews.filter(value = 'UP').count()
        total = reviews.count()
        ratio = (upvote/total)*100
        self.vote_ratio = ratio
        self.vote_total = total

        self.save()

    def __str__(self):
        return self.title
    

class Tag(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Review(models.Model):
    VOTE_TYPE = (
            ("UP", "Up Vote"),
            ("DOWN", "down Vote"),
    )
    owner = models.ForeignKey(Profile, on_delete = models.CASCADE, default='')
    project = models.ForeignKey(Project, on_delete = models.CASCADE)
    review= models.TextField(null=True, blank=True)
    value = models.CharField(max_length = 200, choices = VOTE_TYPE)
    id = models.UUIDField(default = uuid.uuid4, editable = False, unique = True, primary_key = True)
    created = models.DateTimeField(auto_now_add = True)

    class Meta:
        unique_together = [['owner', 'project']]
        

    def __str__(self):
        return self.value