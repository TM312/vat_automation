
from app.extensions import socket_io
from wsgi import celery

from app.namespaces.tax_record.interface import TaxRecordInterface


@celery.task(bind=True, name='api.app.tasks.asyncr.async_create_tax_record_by_seller_firm_public_id')
def async_create_tax_record_by_seller_firm_public_id(self, seller_firm_public_id: str, user_id: int, tax_record_data_raw: TaxRecordInterface):
    #test
    from app.namespaces.tax_record.service import TaxRecordService
    TaxRecordService.create_by_seller_firm_public_id(seller_firm_public_id, user_id, tax_record_data_raw)
