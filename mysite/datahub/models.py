from __future__ import unicode_literals
from django.contrib.auth.models import User
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils.timezone import now


@python_2_unicode_compatible
class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = 'tag'
        verbose_name_plural = 'tags'
        ordering = ['name']

    def __str__(self):
        return self.name


class PublicFolderManager(models.Manager):
    def get_queryset(self):
        qs = super(PublicFolderManager, self).get_queryset()
        return qs.filter(is_public=True)


@python_2_unicode_compatible
class Folder(models.Model):
    label = models.CharField('label', blank=False, max_length=255)
    description = models.TextField('description', blank=True)
    is_public = models.BooleanField('public', default=True)
    date_created = models.DateTimeField('date created')
    date_updated = models.DateTimeField('date updated')
    owner = models.ForeignKey(User, verbose_name='owner', related_name='folders')

    objects = models.Manager()
    public = PublicFolderManager()

    class Meta:
        verbose_name = 'folder'
        verbose_name_plural = 'folders'
        ordering = ['-date_created']

    def __str__(self):
        return self.label

    def save(self, *args, **kwargs):
        if not self.id:
            self.date_created = now()
        self.date_updated = now()
        super(Folder, self).save(*args, **kwargs)



class PublicDocumentManager(models.Manager):
    def get_queryset(self):
        qs = super(PublicDocumentManager, self).get_queryset()
        return qs.filter(is_public=True)


@python_2_unicode_compatible
class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')
    title = models.CharField('title', max_length=255)
    description = models.TextField('description', blank=True)
    is_public = models.BooleanField('public', default=True)
    date_created = models.DateTimeField('date created', blank=True, default='')
    date_updated = models.DateTimeField('date updated', blank=True, default='')
    owner = models.ForeignKey(User, default='', verbose_name='owner',
        related_name='documents')
    folder = models.ManyToManyField(Folder, blank=True)
    tags = models.ManyToManyField(Tag, blank=True)

    objects = models.Manager()
    public = PublicDocumentManager()

    class Meta:
        verbose_name = 'document'
        verbose_name_plural = 'documents'
        ordering = ['-date_created']

    def __str__(self):
        return '%s (%s)' % (self.title, self.owner)

    def save(self, *args, **kwargs):
        if not self.id:
            self.date_created = now()
        self.date_updated = now()
        super(Document, self).save(*args, **kwargs)
