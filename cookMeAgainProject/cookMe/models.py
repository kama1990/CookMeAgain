from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Recipe(models.Model):
    title = models.CharField('Tytuł', max_length=50)
    dishPicture = models.ImageField('Zdjęcie potrawy', blank=True, upload_to='dishPics')
    rating = [
        ('', 'Wybierz ocenę'),
        ('rew', 'Rewelacja'),
        ('nie', 'Nie do powtórzenia'),
        ('mod', 'Do modyfikacji'),

    ]
    myRating = models.CharField('Moja ocena', max_length=3, choices=rating, default='') # choices - the value of this field can be set only to one of the given ones (rating)
    descRecipe = models.TextField('Przepis', blank=True)
    webRecipe = models.URLField('Strona www', max_length=200, blank=True)
    picRecipe = models.ImageField('Zdjęcie przepisu', blank=True, upload_to='recipePics')
    comment = models.TextField('Moje uwagi', blank=True)
    mainComponents = models.TextField('Główne składniki', blank=True)
    createDate = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    class Meta:
        ordering = ('-createDate',) # results sorted descending

    def __str__(self):
        return self.title