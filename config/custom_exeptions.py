import functools
import inspect
import json
import traceback

from django.db import transaction
from django.http import JsonResponse
from django.views import View
import logging
logger = logging.getLogger('ExeptionHunter')

JSON_DUMPS_PARAMS = {
    'ensure_ascii': False
}

def ret(json_object, status=200):
    """ Віддає JSON з правильним HTTP заголовком і в читабельному вигляді для браузера"""
    return JsonResponse(
        json_object,
        status = status,
        safe = not isinstance(json_object, list),
        json_dumps_params = JSON_DUMPS_PARAMS
    ) 
def error_response(exeption):
    """ формує HTTP відповідь з описом помилки """
    res = {'errorMessage': str(exeption),
            # потрібно перевірити чи  DEBUG =FALSE - тоді traceback не виводити в браузер на продакшен
            'traceback': traceback.format_exc()}
    return ret(res, status=400)


def base_view(fn):
    """ Декоратор для всіх помилок """
    @functools.wraps(fn)
    def inner(request, *args, **kwargs):
        try:
            with transaction.atomic():
                return fn(request, *args, **kwargs)
        except Exception as e:
            return error_response(e)

class ExeptionHunter(View):
    """ Клас який відловлює всі помилки """
    def dispatch(self, request, *args, **kwargs):
        try:
            response = super().dispatch(request, *args, **kwargs)
        except Exception as e:
            data={'errorMessage': str(e), 'traceback': traceback.format_exc()}
            logger.error(str(data))
            return self._response(data, status=400)

        if isinstance(response, (dict, list)):
            return self._response(response)
        else:
            return response

    @staticmethod
    def _response(data, *, status=200):
        return JsonResponse(
            data,
            status = status,
            safe = not isinstance(data, list),
            json_dumps_params = JSON_DUMPS_PARAMS
        )  