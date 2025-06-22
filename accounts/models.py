from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class TranslationHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    input_text = models.TextField()
    output_text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)