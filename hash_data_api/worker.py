from celery import Celery

worker = Celery('tasks')
worker.conf.broker_url = 'redis://localhost:6379/0'
worker.conf.result_backend = 'redis://localhost:6379/0'
worker.conf.broker_transport_options = {'visibility_timeout': 3600,
                                    'fanout_prefix': True,
                                     'fanout_patterns': True}


@worker.task
def predict():
    return {'offers.priceSale': 1231231}