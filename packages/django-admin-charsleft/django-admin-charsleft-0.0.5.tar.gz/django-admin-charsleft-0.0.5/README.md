# Django CharsLeft Widgets & Admin Mixin

Inspired from [django-charsleft-widget](https://github.com/timmyomahony/django-charsleft-widget/)
by [Timmy O'Mahony](https://github.com/timmyomahony)
and [django-charsleft-widget](https://github.com/bashu/django-charsleft-widget)
by [Basil Shubin](https://github.com/bashu)


*django-admin-charsleft* provides a simple way to add information to django's admin interface about the remaining
characters for both `CharField` and `TextField` inputs, relying on the `max_length` attribute.

*django-admin-charsleft* - as the name implies - is intended for the use inside [django-admin](), whereas the original
projects provide more generic widgets.

It plays nice with the default django-admin (>=1.9) - and also seamlessly integrates
with [django-slick-admin](https://github.com/palmbeach-interactive/django-slick-admin).

### Screenshot

![display example](docs/img/charsleft-example.png)



### Installation


Using the latest version from PyPI:

    pip install django-admin-charsleft

Using this GitHub repository:

    pip install -e "git://github.com/palmbeach-interactive/django-admin-charsleft.git#egg=django-admin-charsleft"


Then add `charsleft` to `INSTALLED_APPS`.




### Usage

#### As Admin Mixin

*django-admin-charsleft* provides a `CharsLeftAdminMixin` class that can be used to extend your admin classes:


    from charsleft.admin import CharsLeftAdminMixin

    @admin.register(MyModel)
    class MyModelAdmin(CharsLeftAdminMixin, admin.ModelAdmin):
        ...

The mixin can be used on `admin.ModelAdmin` and as well on `admin.TabularInline` and `admin.StackedInline`.
