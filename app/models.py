from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db import models


# ModelManager


class TagManager(models.Manager):
    def hot_tags(self):
        return super().get_queryset().order_by("-rating")


class Tag(models.Model):
    tag = models.CharField(unique=True, max_length=32)
    rating = models.IntegerField(default=0)

    objects = TagManager()

    def __str__(self):
        return self.tag


def user_directory_path(instance, filename):
    # путь, куда будет осуществлена загрузка MEDIA_ROOT/user_<id>/<filename>
    return 'uploads/user_{0}/{1}'.format(instance.user.id, filename)


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    avatar = models.ImageField(default="icons/no_name.png", upload_to=user_directory_path)

    def __str__(self):
        return str(self.user)


class QuestionManager(models.Manager):
    def hot(self):
        return super().get_queryset().order_by("-rating")

    def all(self):
        return super().get_queryset().order_by("-datetime")

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("question", kwargs={"pk": self.pk})

    def by_tag(self, tag):
        return self.filter(tags__tag=tag).order_by("-rating")


class Question(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, related_name='questions',
                                related_query_name='question')
    datetime = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=256)
    text = models.TextField()
    tags = models.ManyToManyField('Tag')
    number_of_answers = models.IntegerField(default=0)
    rating = models.IntegerField(default=0)
    likes_count = models.IntegerField(default=0)
    dislikes_count = models.IntegerField(default=0)

    objects = QuestionManager()

    def __str__(self):
        return self.title

    # class Meta:
    #     ordering = ["-datetime"]


class AnswerManager(models.Manager):
    def by_question(self, pk):
        return self.filter(question_id=pk).order_by("-rating")


class Answer(models.Model):
    profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)
    text = models.TextField()
    is_correct = models.BooleanField(default=False)
    rating = models.IntegerField(default=0)
    likes_count = models.IntegerField(default=0)
    dislikes_count = models.IntegerField(default=0)

    objects = AnswerManager()

    def save(self, *args, **kwargs):
        if not self.pk:
            self.question.number_of_answers += 1
            self.question.save()
        super(Answer, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.question_id.number_of_answers -= 1
        self.question_id.save()
        super(Answer, self).delete(*args, **kwargs)

    def __str__(self):
        return str(self.question)


class LikeQuestion(models.Model):
    question_id = models.ForeignKey('Question', on_delete=models.CASCADE)
    profile_id = models.ForeignKey('Profile', on_delete=models.CASCADE)
    is_like = models.BooleanField(default=True)


class LikeAnswer(models.Model):
    answer_id = models.ForeignKey('Answer', on_delete=models.CASCADE)
    profile_id = models.ForeignKey('Profile', on_delete=models.CASCADE)
    is_like = models.BooleanField(default=True)
