# -*- coding: utf-8 -*-
# @Time: 2025/10/29 22:29
# @Author: lxc
# @File: AsyncOdesli.py
# @Software: PyCharm
from odesli.Odesli import Odesli
import aiohttp
from functools import cached_property

from odesli.Odesli import ROOT, LINKS_ENDPOINT
from odesli.entity.EntityResult import EntityResult
from odesli.entity.album.AlbumResult import AlbumResult
from odesli.entity.song.SongResult import SongResult


class AsyncOdesli(Odesli):

    def __init__(self, key=None, proxy: str = None):
        """
        :param key: Your Odesli API key.
        """
        super().__init__(key)
        self.proxy = proxy

    async def __get(self, params) -> EntityResult:
        if self.key is not None:
            params['key'] = self.key
        resp = await self.session.get(f'{ROOT}/{LINKS_ENDPOINT}', params=params)
        result = await resp.json()
        result_type = next(iter(result['entitiesByUniqueId'].values()))['type']
        if result_type == 'song':
            return SongResult.parse(result)
        elif result_type == 'album':
            return AlbumResult.parse(result)
        else:
            raise NotImplementedError(f'Entities with type {result_type} are not supported yet.')

    async def getByUrl(self, url: str) -> EntityResult:
        return await self.__get({'url': url})

    async def close(self):
        pass

    @cached_property
    def session(self):
        return aiohttp.ClientSession(proxy=self.proxy)


if __name__ == '__main__':
    import asyncio


    async def main():
        odesli = AsyncOdesli()
        result = await odesli.getByUrl('https://music.apple.com/us/song/the-fate-of-ophelia/1833328840')
        print(result)
        await odesli.session.close()


    asyncio.run(main())
