from django.contrib import admin
from django.utils.safestring import mark_safe

from .models import Category, Genre, Actor, Movie, RatingStar, Rating, Review, MovieShots


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug')
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'get_photo')
    readonly_fields = ('get_photo',)

    def get_photo(self, obj):
        return mark_safe(f'<img src="{obj.image.url}" width="50">')

    get_photo.short_description = "Изображение"


class ReviewInline(admin.TabularInline):
    model = Review
    extra = 0
    readonly_fields = ('name', 'email')


class MovieShotsInline(admin.TabularInline):
    model = MovieShots
    extra = 0
    readonly_fields = ('get_photo',)

    def get_photo(self, obj):
        return mark_safe(f'<img src="{obj.images.url}" width="110">')

    get_photo.short_description = "Миниатюра"


@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'slug', 'year', 'draft')
    prepopulated_fields = {"slug": ("title",)}
    list_filter = ('category', 'year')
    search_fields = ('title', 'category__title')
    list_editable = ('draft',)
    actions = ["publish", "unpublished"]
    readonly_fields = ("get_photo",)
    inlines = [MovieShotsInline, ReviewInline]
    save_on_top = True
    fieldsets = (
        (None, {
            "fields": (("title", "tagline"),)
        }),
        (None, {
            "fields": ("description", ("poster", "get_photo"))
        }),
        (None, {
            "fields": ("year", "world_premiere", "country")
        }),
        ("Актеры и режиссеры", {
            "classes": ("collapse",),
            "fields": (("actors", "directors", "genres", "category"),)
        }),
        (None, {
            "fields": (("budget", "fees_in_usa", "fees_in_world"),)
        }),
        (None, {
            "fields": (("slug", "draft"),)
        }),
    )

    def get_photo(self, obj):
        return mark_safe(f'<img src="{obj.poster.url}" width="110">')

    get_photo.short_description = "Миниатюра"

    def unpublished(self, request, queryset):
        """ Снять с публикации """
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = "1 записей была обновлена"
        else:
            message_bit = f'{row_update} записей были обновлены'
        self.message_user(request, f'{message_bit}')

    def publish(self, request, queryset):
        """ Снять с публикации """
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = "1 записей была обновлена"
        else:
            message_bit = f'{row_update} записей были обновлены'
        self.message_user(request, f'{message_bit}')

    unpublished.short_description = 'Снять с публикации'
    unpublished.allowed_permissions = ('change',)

    publish.short_description = 'Опубликовать'
    publish.allowed_permissions = ('change',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'slug')
    list_display_links = ('id', 'title')
    prepopulated_fields = {"slug": ("title",)}


@admin.register(Review)
class ReviewsAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'parent', 'movie', 'id')
    readonly_fields = ('name', 'email')


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('star', 'movie', 'ip')


@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    list_display = ('title', 'movie', 'get_photo')
    readonly_fields = ('get_photo',)

    def get_photo(self, obj):
        return mark_safe(f'<img src="{obj.images.url}" width="75">')

    get_photo.short_description = "Изображение"


@admin.register(RatingStar)
class RatingStarAdmin(admin.ModelAdmin):
    list_display = ('value',)


admin.site.site_header = "Django Movies"
