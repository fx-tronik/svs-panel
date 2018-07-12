from mysite.celery import app



@app.task
def Test():
    from . import mqtt
    mqtt.client.loop_start()
    print('test1')

@app.task
def Test1():
    from . import mqtt
    mqtt.client2.loop_start()
    print('test2')
