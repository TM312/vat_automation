import random
import time

from app.extensions import socket_io
from wsgi import celery

from app.namespaces.tax.vatin.interface import VATINInterface

# Celery creates task names based on how module is imported. It is a little dangerous.
# Set explicitly name for every task. Prefer using proj.package.module.function_name convention to avoid collisions with 3rd party packages.
# https://pawelzny.com/python/celery/2017/08/14/celery-4-tasks-best-practices/
@celery.task(bind=True, name='api.app.tasks.asyncr.async_process_validation_request')
def async_process_validation_request(self, vatin_data: VATINInterface):
    from app.namespaces.tax.vatin.service import VATINService
    VATINService.process_validation_request(vatin_data)
