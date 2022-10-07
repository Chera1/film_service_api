import uuid
from typing import Optional, Union, Tuple

from aioredis import Redis
from elasticsearch import AsyncElasticsearch, NotFoundError
from elasticsearch.exceptions import RequestError
from fastapi import Depends, Request

from db.elastic import get_elastic
from db.redis import get_redis
from models.genre import Genre
from utils.cache import AbstractCache, RedisCache
from utils.sort_string import clear_sort_string


class GenreService:
    """GenreService содержит бизнес-логику по работе с жанрами."""

    def __init__(self, cache: AbstractCache, elastic: AsyncElasticsearch):
        self.elastic = elastic
        self.cache = cache

    async def get_genre_by_id(self, genre_id: uuid.UUID) -> Optional[Genre]:
        """
        Получаем жанр по uuid

        @param genre_id: uuid жанра
        @return: объект-жанр
        """
        genre = await self.cache.get()

        if not genre:
            try:
                genre = await self.elastic.get('genres', genre_id)
            except NotFoundError:
                return None
            await self.cache.set(genre)

        genre = Genre(**genre['_source'])
        return genre

    async def get_genres(
            self,
            sort: Optional[str] = None,
            limit: Optional[int] = 50,
            page: Optional[int] = 1,
    ) -> Tuple[Union[list[Genre], None], list[str]]:
        """
        Получает список жанров

        @param sort: имя поля по которому идет сортировка
        @param limit: количество записей на странице
        @param page: номер страницы
        @return: Данные по жанрам
        """

        errors = []
        query_ = None

        genres = await self.cache.get()

        if not genres:
            sort = clear_sort_string(sort, 'name')
            try:
                genres = await self.elastic.search(
                    index='genres',
                    body=query_,
                    size=limit,
                    sort=sort,
                    from_=limit * (page - 1)
                )
                genres = genres['hits']['hits']

                await self.cache.set(genres)

            except RequestError:
                genres = None
                errors.append('В запрашиваемых параметрах содержатся ошибки')

        return genres, errors


def get_genre_service(
        request: Request,
        redis: Redis = Depends(get_redis),
        elastic: AsyncElasticsearch = Depends(get_elastic),
) -> GenreService:
    """
    Провайдер GenreService,
    с помощью Depends он сообщает, что ему необходимы Redis и Elasticsearch
    """
    return GenreService(RedisCache(redis, request), elastic)
