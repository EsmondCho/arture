from django.db import models

from djangotoolbox.fields import ListField, EmbeddedModelField


def content_file_name(instance, filename):
    return ''.join(['profile_pictures/', instance.email, '_', filename])


class User(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    pwd = models.CharField(max_length=30)
    gender = models.BooleanField()
    birth = models.CharField(max_length=8, null=True)
    address = models.TextField(null=True)
    registered_time = models.DateTimeField(auto_now_add=True)
    pic = models.ImageField(null=True, upload_to=content_file_name, default='profile_pictures/default_picture/default.png')
    friend_list = ListField()
    friend_request_list = ListField(EmbeddedModelField('Request'), null=True)
    arture_list = ListField() # insert arture ObjectId
    article_list = ListField() # insert article ObjectId


class Request(models.Model):
    friend_id = models.CharField(max_length=30) # insert objectId
    request_type = models.IntegerField() # request : 1(w), 2(a), 3(r) / requested : 4(w), 5(a), 6(r)


class Article(models.Model):
    user_id = models.CharField(max_length=30) # insert user_objectId
    tag = models.CharField(max_length=30) # insert arture objectId
    text = models.TextField(null=True)
    image = models.ImageField(null=True, upload_to='article_pictures')
    emotion_list = ListField(null=True)
    comment_list = ListField(EmbeddedModelField('Comment'), null=True)
    #config = models.CharField(max_length=30)
    registered_time = models.DateTimeField(auto_now_add=True)

    def save(self, force_insert=False, force_update=False, using=None):
        for field in self._meta.fields:
            if field.name == 'image':
                field.upload_to = 'article_pictures/%s' % self.user_id
        super(Article, self).save()


class Comment(models.Model):
    author = models.CharField(max_length=30) # insert user_objectId
    comment = models.TextField(null=True)
    registered_time = models.DateTimeField(auto_now_add=True)


class Arture(models.Model):
    title = models.CharField(max_length=30)
    image = models.ImageField(null=True, upload_to='arture_pictures')
    article_list = ListField(null=True)
    user_list = ListField(null=True)
    arture_type = models.BooleanField() # True : artist / False : art
    description = models.TextField(null=True)
    related_arture_list = ListField() # Insert Arture ObjectId

    def save(self, force_insert=False, force_update=False, using=None):
        for field in self._meta.fields:
            if field.name == 'image':
                field.upload_to = 'arture_pictures/%s' % self.title
        super(Arture, self).save()
