from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

# Create your models here.
class Recipe(models.Model):
    title = models.CharField('Tytuł', max_length=50)
    dish_picture = models.ImageField('Zdjęcie potrawy', blank=True, upload_to='dishPics')
    rating = [
        ('', 'Wybierz ocenę'),
        ('rew', 'Rewelacja'),
        ('nie', 'Nie do powtórzenia'),
        ('mod', 'Do modyfikacji'),

    ]
    my_rating = models.CharField('Moja ocena', max_length=3, choices=rating, default='') # choices - the value of this field can be set only to one of the given ones (rating)
    desc_recipe = models.TextField('Przepis', blank=True)
    web_recipe = models.URLField('Strona www', max_length=200, blank=True)
    pic_recipe = models.ImageField('Zdjęcie przepisu', blank=True, upload_to='recipePics')
    comment = models.TextField('Moje uwagi', blank=True)
    main_components = models.TextField('Główne składniki', blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


    class Meta:
        ordering = ('-create_date',) # results sorted descending

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('post_detail',
                       args=[self.id])