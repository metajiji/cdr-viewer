# DEVELOPMENT

## Initial create project:

```bash
virtualenv -p python2 --prompt="(cdr-viewer)" venv
pip install --upgrade pip
django-admin startproject cdr .
python manage.py migrate
python manage.py createsuperuser
python manage.py collectstatic
```

## If `models.py` was chenged, run again:

```bash
python manage.py makemigrations cdr
python manage.py migrate
```

## Custom admin

### Create custom admin area for manage users:
```bash
django-admin.py startapp customuseradmin
```
#### Code `customuseradmin/admin.py`:
```
# -*- coding:utf-8 -*-
from django.contrib import admin
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin

admin.site.unregister(User)

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'is_staff','is_active',)
    list_filter = ('is_staff', 'is_superuser', 'is_active',)
admin.site.register(User, CustomUserAdmin)
```

## Test **SMTP** Email Server

### Run server:
```bash
python -m smtpd -n -c DebuggingServer localhost:1025
```

## Localization

### Compile `.mo` files from `.po`:
```bash
find accounts/locale -name *.po | sed 's/\.po$//g' | xargs -i{} msgfmt {}.po -o {}.mo
```

## Git delete unwanted file from repo

`Be careful! This will overwrite your existing tags.`
```
git filter-branch --force --index-filter \
'git rm --cached --ignore-unmatch cdr/settings.py' \
--prune-empty --tag-name-filter cat -- --all
```