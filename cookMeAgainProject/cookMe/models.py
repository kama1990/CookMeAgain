from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.template.defaultfilters import slugify

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,
                            unique=True)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
        ]
        verbose_name = 'category'
        verbose_name_plural = 'categories'

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if self.name:
            self.slug = slugify(self.name)

        super(Category, self).save(*args, **kwargs)


    def get_absolute_url(self):
        return reverse('post_recipe_by_category',
                       args=[self.slug])
    

class Recipe(models.Model):
    RATING=[
        ('', 'Wybierz ocenę'),
        ('REWELACJA', 'Rewelacja'),
        ('NIE DO POWTÓRZENIA', 'Nie do powtórzenia'),
        ('DO MODYFIKACJI', 'Do modyfikacji'),

    ]

    category = models.ForeignKey(to=Category,
                                 related_name='recipes',
                                 on_delete=models.CASCADE)
    title = models.CharField('Tytuł', max_length=100)
    slug = models.SlugField(max_length=100)
    dish_picture = models.ImageField('Zdjęcie potrawy', blank=True, upload_to='dishPics')
    
    my_rating = models.CharField('Moja ocena',max_length=20,choices=RATING, default='') # choices - the value of this field can be set only to one of the given ones (rating)
    desc_recipe = models.TextField('Przepis', blank=True)
    web_recipe = models.URLField('Strona www', max_length=200, blank=True)
    pic_recipe = models.ImageField('Zdjęcie przepisu', blank=True, upload_to='recipePics')
    comment = models.TextField('Moje uwagi', blank=True)
    main_components = models.TextField('Główne składniki', blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(to=User,on_delete=models.CASCADE)


    class Meta:
        ordering = ['title'] # results sorted descending
        indexes = [
            models.Index(fields=['id', 'slug']),
            models.Index(fields=['title']),
            models.Index(fields=['-create_date']),
        ]
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.title:
            self.slug = slugify(self.title)

        super(Recipe, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('post_detail',
                       args=[self.id, self.slug])