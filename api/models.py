from django.db import models



class Posts(models.Model):
    title=models.CharField(max_length=120)
    description=models.CharField(max_length=120)
    image=models.ImageField(upload_to="postimages",null=True)
    user=models.CharField(max_length=120)
    date=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title