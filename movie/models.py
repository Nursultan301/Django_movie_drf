from django.db import models
from datetime import date
from ckeditor_uploader.fields import RichTextUploadingField

from django.urls import reverse


class Category(models.Model):
    """ Категория """
    title = models.CharField("Категория", max_length=50, unique=True)
    description = models.TextField("Описание", blank=True)
    slug = models.SlugField("URL", unique=True)

    objects = models.Manager

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"

    def __str__(self):
        return self.title


class Actor(models.Model):
    """ Актеры и режиссеры """
    name = models.CharField("Имя", max_length=50)
    age = models.PositiveSmallIntegerField("Возраст", default=0)
    description = models.TextField("Описание", blank=True)
    image = models.ImageField("Изображение", upload_to="actors/")

    def get_absolute_url(self):
        return reverse('actor_detail', kwargs={'slug': self.name})

    class Meta:
        verbose_name = "Актеры и режиссеры"
        verbose_name_plural = "Актеры и режиссеры"

    def __str__(self):
        return self.name


class Genre(models.Model):
    """ Жанр """
    title = models.CharField("Называние", max_length=50, unique=True)
    description = models.TextField("Описание", blank=True)
    slug = models.SlugField("URL", unique=True)

    objects = models.Manager

    class Meta:
        verbose_name = "Жанр"
        verbose_name_plural = "Жанры"

    def __str__(self):
        return self.title


class Movie(models.Model):
    """ Фильм """
    title = models.CharField("Называние", max_length=50, unique=True)
    tagline = models.CharField("Слоган", max_length=100, default="")
    description = RichTextUploadingField("Описание")
    poster = models.ImageField("Постер", upload_to="movies/")
    year = models.PositiveSmallIntegerField("Дата выхода", default=2021)
    country = models.CharField("Страна", max_length=30)
    directors = models.ManyToManyField(Actor, related_name='film_director', verbose_name="Режиссер")
    actors = models.ManyToManyField(Actor, related_name='film_actor', verbose_name="Актер")
    genres = models.ManyToManyField(Genre, verbose_name="Жанры")
    world_premiere = models.DateField("Примера в мире", default=date.today)
    budget = models.PositiveIntegerField("Бюджет", default=0, help_text="Указывать сумму в долларах")
    fees_in_usa = models.PositiveIntegerField("Сборы в США", default=0, help_text="Указывать сумму в долларах")
    fees_in_world = models.PositiveIntegerField("Сборы в мире", default=0, help_text="Указывать сумму в долларах")
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, verbose_name="Категория")
    slug = models.SlugField("URL", max_length=50, unique=True)
    draft = models.BooleanField("Черновик", default=False)

    objects = models.Manager

    class Meta:
        verbose_name = "Фильм"
        verbose_name_plural = "Фильмы"

    def get_absolute_url(self):
        return reverse('movie_detail', kwargs={'slug': self.slug})

    def __str__(self):
        return self.title

    # Это функция вернутся только родительский отзывы

    def get_review(self):
        return self.review_set.filter(parent__isnull=True)


class MovieShots(models.Model):
    """ Кадры из фильма """
    title = models.CharField("Заголовок", max_length=50)
    description = models.TextField("Описание")
    images = models.ImageField("Изображение", upload_to="movie_shots/")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name="Фильм", related_name='movieshots')

    class Meta:
        verbose_name = "Кадры из фильма"
        verbose_name_plural = "Кадры из фильма"

    def __str__(self):
        return self.title


class RatingStar(models.Model):
    """ Звезда рейтинга """
    value = models.PositiveSmallIntegerField("Значение", default=0)

    class Meta:
        verbose_name = "Звезда рейтинга"
        verbose_name_plural = "Звезды рейтинга"
        ordering = ['-value']

    def __str__(self):
        return f'{self.value}'


class Rating(models.Model):
    """ Рейтинг """
    ip = models.CharField("IP адрес", max_length=15)
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE, verbose_name="Звезда")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name="Фильм")

    class Meta:
        verbose_name = "Рейтинг"
        verbose_name_plural = "Рейтинги"

    def __str__(self):
        return f'{self.star} - {self.movie}'


class Review(models.Model):
    """ Отзыв """
    email = models.EmailField("E-mail")
    name = models.CharField("Имя", max_length=50)
    text = models.TextField(max_length=5000)
    parent = models.ForeignKey("self", on_delete=models.SET_NULL, blank=True, null=True, verbose_name="Родитель")
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, verbose_name="Фильм", related_name="reviews")

    class Meta:
        verbose_name = "Отзыв"
        verbose_name_plural = "Отзывы"

    def __str__(self):
        return f'{self.name} - {self.movie}'
