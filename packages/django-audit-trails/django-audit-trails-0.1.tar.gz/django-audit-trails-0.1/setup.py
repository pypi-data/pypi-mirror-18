from distutils.core import setup

setup(
    name = 'django-audit-trails',
    packages = ['django_audit'],
    version = '0.1',
    description = 'A simple audit log pattern for django apps that doesnt conflict with migrations',
    author = 'Shean Massey',
    author_email = 'shean.massey@gmail.com',
    url = 'https://github.com/sheanmassey/django-audit-trails',
    download_url = 'https://github.com/sheanmassey/django-audit-trails/tarball/0.1',
    keywords = ['audit', 'logging', 'audit trails', 'audit log'],
    classifiers = [],
)
