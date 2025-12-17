from django.db import models
import json

class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    face_image = models.ImageField(upload_to='faces/', null=True, blank=True)  # store face photo
    face_encoding = models.TextField(null=True, blank=True)  # NEW field to store encoding

    def __str__(self):
        return self.name

    def set_encoding(self, encoding):
        self.face_encoding = json.dumps(encoding)

    def get_encoding(self):
        if self.face_encoding:
            return json.loads(self.face_encoding)
        return None
