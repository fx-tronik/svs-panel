import json
from .models import Infrasctructure, Zone, Alert
from django.core.exceptions import ObjectDoesNotExist, MultipleObjectsReturned
from .logger import logger
from . import tasks
from mysite.celery import app

allowed_infrastuctures = ('DI', 'DO', 'AI', 'AO')


def svs_callback(payload):

    try:
        dict = json.loads(str(payload.decode("utf-8", "ignore")))
    except json.JSONDecodeError:
        logger.critical("Nieprawidlowy obiekt")
        return

    dict = json.loads(str(payload.decode("utf-8", "ignore")))
    for type in dict:
        if type in allowed_infrastuctures:
            for i, value in enumerate(dict[type]):
                infrastructure, created = Infrasctructure.objects.get_or_create(type=type, no=i+1)
                infrastructure.value = value
                infrastructure.save()
        else:
            logger.critical("Niedozwolony typ infrastruktury")

def zones_counter(payload):
    logger.debug(payload)
    try:
        dict = json.loads(str(payload.decode("utf-8", "ignore")))
        dane = {'alerts': [] }
    except json.JSONDecodeError:
        logger.critical("Nieprawidlowy obiekt")
        return

    for id, data in dict.items():
        try:
            zone = Zone.objects.get(id=id)
        except ObjectDoesNotExist:
            logger.critical("Strefa o ID: %s nie istnieje" % id)
            return
        except MultipleObjectsReturned:
            logger.critical("Odnaleziono wiele stref o ID: %s" % id)
            return
        except ValueError:
            logger.critical("Nieprawidlowy format wiadomości")
            logger.critical(payload)
            return

        if not zone is None:
            if int(data) > zone.max_human_silhouettes_no:
                logger.critical("[PLACEHOLDER] Wykonaj akcje przypisane do strefy %s" % zone.__str__())

                for alert in Alert.objects.filter(zone=zone).all():
                    dict1 = {}
                    for component in alert.component_action.all():

                        id = (component.arm_output.arm_id)
                        task = (component.arm_task.arm_task)
                        dict1['component-id'] = id
                        dict1['action'] = task

                    dane['alerts'].append(dict1)

            else:
                for alert in Alert.objects.filter(zone=zone).all():
                    dict1 = {}
                    for component in alert.component_action.all():

                        id = (component.arm_output.arm_id)
                        task = (component.arm_task.arm_task)
                        dict1['component-id'] = id
                        dict1['action'] = "off"

                    dane['alerts'].append(dict1)


    if len(dane['alerts']) > 0:
        json_obj = json.dumps(dane)
        tasks.mqtt_send.delay('ws-arm/alerts', json_obj)


# Funckje zbierające tematy


def ws_arm_parse(topic, payload):

    switcher = {
        'svs_callback': lambda: svs_callback(payload),
        'alerts': lambda: logger.info('loopback')
    }

    method = switcher.get(topic, lambda: logger.critical("Nieznany sub-topic %s" %topic))
    return method()


def cv_ws_parse(topic, payload):

    switcher = {
        'zones_counter': lambda: zones_counter(payload),

    }

    method = switcher.get(topic, lambda: logger.critical("Nieznany sub-topic %s" %topic))
    return method()

@app.task
def mqtt_parser(topic, payload):

    main_topic, sub_topic = topic.split('/')

    switcher = {
        'cv-ws': lambda: cv_ws_parse(sub_topic, payload),
        'ws-arm': lambda: ws_arm_parse(sub_topic, payload)
    }

    # Nigdy nie powinno się przytrafić - chyba że subskrybujemy temat dla
    # którego nie napisano obsługi
    method = switcher.get(main_topic, lambda: logger.critical("Nieznany topic"))
    return method()
