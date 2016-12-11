# Always prefer setuptools over distutils
from setuptools import setup, find_packages


setup(
    name='HouseShare',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='1.0.0',

    description='Stream 3 Project',


    # The project's main homepage.
    url='https://github.com/mariahynes/HouseShare',

    # Author details
    author='Maria Hynes | Databasis',
    author_email='maria@databasis.ie',


    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(),

    # Alternatively, if you want to distribute just a my_module.py, uncomment
    # this:
    #   py_modules=["my_module"],

    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['arrow','beautifulsoup4','django-disqus','Django', 'django-emoticons','django-forms-bootstrap',
                      'djangorestframework','django-tinymce','funcsigs','mock','MonthDelta','pbr','Pillow',
                      'python-dateutil','requests','six','sqlparse','wheel','stripe','gunicorn'],





)