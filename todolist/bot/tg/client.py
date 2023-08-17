import logging

from django.conf import settings
import requests
from pydantic import ValidationError

from bot.tg.schemas import GetUpdatesResponse, SendMessageResponse

logger = logging.getLogger(__name__)


class TgClientError(Exception):
    pass


class TgClient:

    '''
        class for interacting with telegram
    '''

    def __init__(self, token: str | None = None):
        self.__token = token if token else settings.BOT_TOKEN
        self.__url = f'https://api.telegram.org/bot{self.__token}/'

    def __get_url(self, method: str) -> str:
        '''
            interaction occurs through the formation of url
        '''
        return f'{self.__url}{method}'

    def get_updates(self, offset: int = 0, timeout: int = 60, **kwargs) -> GetUpdatesResponse:
        '''
            getting data going through, getting the latest updates
        '''

        data = self._get('getUpdates', offset=offset, timeout=timeout, **kwargs)
        return self._serialize_tg_response(GetUpdatesResponse, data)


    def send_message(self, chat_id: int, text: str, **kwargs) -> SendMessageResponse:
        data = self._get('sendMessage', chat_id=chat_id, text=text, **kwargs)
        return self._serialize_tg_response(SendMessageResponse, data)

    def _get(self, method: str, **params) -> dict:
        '''
            query execution
        '''
        url = self.__get_url(method)
        params.setdefault('timeout', 10)
        response = requests.get(url, params=params)
        if not response.ok:
            logger.warning('Invalid status code %d from command %s', response.status_code, method)
            raise TgClientError
        return response.json()

    @staticmethod
    def _serialize_tg_response(serializer_class, data: dict):
        try:
            return serializer_class(**data)
        except ValidationError:
            logger.error('Failed to serialize telegram response', data)
            raise TgClientError
