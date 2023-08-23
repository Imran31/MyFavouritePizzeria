from time import sleep
from celery import shared_task
from django.db import IntegrityError

@shared_task
def initiate_long_task(order_id, old_status, new_status, modifier=1):
    from base.models import Order, Task
    STATUS_MAP = dict(Order.STATUSES)
    MINUTES_MAP = {
        0 : { 1: 0 },
        1 : { 2: 0 },
        2 : { 3: 1 },
        3 : { 4: 3 },
        4 : { 5: 5 },
    }
    if old_status == 5:
        return 'All task completed for order id {}'.format(order_id)
    minutes = MINUTES_MAP[old_status][new_status] * modifier
    task = Task.objects.filter(order_id=order_id, old_value=old_status, new_value=new_status)
    if task.exists():
        return
    try:
        print('*'*10)
        print('Task initiated for {} to {}!'.format(STATUS_MAP[old_status], STATUS_MAP[new_status]))
        print('Will take {} minutes to complete'.format(minutes))
        print('*'*10)
        Task.objects.create(order_id=order_id, old_value=old_status, new_value=new_status)
        sleep(60*minutes)
        Order.objects.filter(id=order_id).update(status=new_status)
        initiate_long_task.delay(order_id, new_status, new_status + 1, modifier)
    except IntegrityError:
        print('Task already added')
        return
    return 'Task changed from {} to {}'.format(STATUS_MAP[old_status], STATUS_MAP[new_status])
