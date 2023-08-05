from setuptools import setup, find_packages

setup(
    name='jmbo',
    version='2.0.17',
    description='The Jmbo base product introduces a content type and various tools required to build Jmbo products.',
    long_description = open('README.rst', 'r').read() + open('AUTHORS.rst', 'r').read() + open('CHANGELOG.rst', 'r').read(),
    author='Praekelt Consulting',
    author_email='dev@praekelt.com',
    license='BSD',
    url='http://www.jmbo.org',
    packages = find_packages(),
    install_requires = [
        # The bare minimum requirements. The tests use explicit versions.
        'Pillow',
        'pytz',
        'django>=1.4,<1.7',
        'django-category>=0.0.5',
        'django-likes>=0.0.8',
        'django-preferences',
        'django-publisher',             # legacy, required by migrations
        'django-sites-groups',
        'django-tastypie>=0.10,<0.12',  # 0.12 requires Django 1.7
        'django-celery',
        'django-generate',
        'django-pagination',
        'django-photologue>=3.1,<3.2',
        'django-ultracache',
        'south',
    ],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Development Status :: 4 - Beta",
        "Operating System :: OS Independent",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
    ],
    zip_safe=False,
)
