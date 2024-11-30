from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator

class Content(models.Model):
    title = models.CharField(max_length=255)
    metadata = models.JSONField(default=dict)
    rating = models.DecimalField(
        max_digits=4, 
        decimal_places=2, 
        validators=[MinValueValidator(0), MaxValueValidator(10)]
    )

    def __str__(self):
        return self.title


class ContentFile(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='files')
    file = models.FileField(upload_to='content_files/')

    def __str__(self):
        return f"File for {self.content.title} - {self.file.name}"


class Channel(models.Model):
    title = models.CharField(max_length=255)
    language = models.CharField(max_length=100)
    picture = models.ImageField(upload_to='channel_pictures/', blank=True, null=True)
    parent_channel = models.ForeignKey(
        'self', on_delete=models.CASCADE, related_name='subchannels', blank=True, null=True
    )
    contents = models.ManyToManyField(Content, blank=True)

    def clean(self):
        if self.pk is None:
            return
        if self.subchannels.exists() and self.contents.exists():
            raise ValidationError("A channel cannot have both subchannels and contents.")

        if not self.subchannels.exists() and not self.contents.exists():
            raise ValidationError("A channel must have at least one content or one subchannel.")

    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
