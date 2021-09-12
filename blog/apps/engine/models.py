from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse
from django.utils import timezone


class Post(models.Model):
    """Model representing a post to the blog."""
    class Status(models.IntegerChoices):
        DRAFT = 1
        PUBLISHED = 2
        HIDDEN = 3

    author = models.ForeignKey(User, on_delete=models.CASCADE, editable=False)
    title = models.CharField(max_length=200)
    slug = models.SlugField()
    content = models.TextField()
    status = models.SmallIntegerField(choices=Status.choices, default=Status.DRAFT)
    published_at = models.DateTimeField(editable=False, null=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-published_at',)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        if self.published_at is None:
            raise NotImplementedError('TODO')
            
        return reverse(
            'permalink',
            kwargs={
                'year': self.published_at.strftime('%Y'),
                'month': self.published_at.strftime('%m'),
                'day': self.published_at.strftime('%d'),
                'slug': self.slug,
            }
        )

    @property
    def is_draft(self):
        """Gets whether or not this post is an unpublished draft."""
        return self.status == Post.Status.DRAFT

    @property
    def is_published(self):
        """Gets whether or not this post is published to the site."""
        return self.status == Post.Status.PUBLISHED

    def save(self, *args, **kwargs):
        """
        Synchronizes the post's publication time with model state in addition to standard 
        Model.save() behavior.
        
        """
        self._set_published_at()
        super().save(*args, **kwargs)

    def _set_published_at(self):
        """Sets the post's publication time to an appropriate value based on its current status.
        
        Normally, the publication time is that of the first save where the status
        variable is set to PUBLISHED. In the case of a post where status is set to
        DRAFT after initial publication, it is assumed the original publication was in error 
        and the actual publication time will be when the status is reset to PUBLISHED. 
        Accordingly, published_at should be set to None whenever status is DRAFT.

        HIDDEN posts that were previously published retain their original
        publication times. The logic here is a PUBLISHED -> HIDDEN -> PUBLISHED 
        workflow is expected to occur when a post requires a major update. 
        Accordingly, timestamps should emphasize the new version is an 
        update and not a brand-new entry.

        """
        if self.is_published and self.published_at is None:
            self.published_at = timezone.now()
        elif self.is_draft:
            self.published_at = None
