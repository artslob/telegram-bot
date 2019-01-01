from abc import ABC, abstractmethod

import aiohttp

import config


class AbstractMethod(ABC):
    default_timeout = aiohttp.ClientTimeout(total=20)

    @classmethod
    @abstractmethod
    def method_address(cls) -> str:
        pass

    @classmethod
    def api_address(cls) -> str:
        return f'{config.API}/{cls.method_address()}'

    @classmethod
    def post_json(cls, json: dict):
        headers = {
            'Content-Type': 'application/json'
        }
        url = cls.api_address()
        params = dict(url=url, json=json, headers=headers)
        return aiohttp.request('POST', **params, timeout=cls.default_timeout)


class SetWebhookMethod(AbstractMethod):
    @classmethod
    def method_address(cls) -> str:
        return 'setWebhook'


class SendMessageMethod(AbstractMethod):
    @classmethod
    def method_address(cls) -> str:
        return 'sendMessage'
