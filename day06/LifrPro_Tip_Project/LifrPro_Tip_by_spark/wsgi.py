"""
WSGI config for LifrPro_Tip_by_spark project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'LifrPro_Tip_by_spark.settings')

application = get_wsgi_application()
