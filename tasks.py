from celery import shared_task


@shared_task(ignore_result=False)
def celery_test(x, y):
    print("celery test invoked")

    return x + y