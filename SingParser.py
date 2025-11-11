# -*- coding: utf-8 -*-
# @Time: 2025/10/30 21:29
# @Author: lxc
# @File: SingParser.py
# @Software: PyCharm
import tldextract
from setting import get_config_value
from urllib.parse import urlparse
from asyncio import Semaphore
from functools import lru_cache
from music_parse import BaseProvider, ProviderRegistry

ALL_PROVIDERS = get_config_value("provider")
ALL_PROVIDERS_MAPPING = {v: k for k, v in ALL_PROVIDERS.items()}
ODESLI_PROVIDERS = get_config_value("Odesli", "provider")


class SingParser:
    def __init__(self, sem_num: int = 10):
        self.sem = Semaphore(sem_num)
        self.use_odesli: bool = get_config_value("crawler", "use_odesli")

    async def parse(self, url: str) -> dict:
        async with self.sem:
            return await self._parse(url)

    async def _parse(self, url: str) -> dict:
        if self.use_odesli:
            is_odesli = self.is_supported_by_odesli(url)
            if is_odesli:
                parser_cls = self.get_parser("defaultprovider")
                async with parser_cls() as p:
                    try:
                        result = await p.parse(url)
                        if result:
                            return result
                    except Exception as e:
                        print(e)
        provider_name = self.get_provider_name(url)
        if not provider_name:
            print(f"不支持的url: {url}")
            raise NotImplementedError("不支持的url")
        parser_cls = self.get_parser(provider_name)
        async with parser_cls() as p:
            return await p.parse(url)

    @staticmethod
    def get_parser(provider_name: str) -> type[BaseProvider]:
        cls = ProviderRegistry.get_parser(provider_name)
        if cls:
            return cls
        else:
            raise NotImplementedError(f"{provider_name} not implemented")

    def get_provider_name(self, url: str) -> str | None:
        """
        :param url:
        :return:
        """
        domain = urlparse(url).hostname
        return self._get_provider_name(domain)

    @lru_cache()
    def _get_provider_name(self, domain: str) -> str | None:
        """
        :param domain:
        :return:
        """
        # if domain.startswith("www."):
        #     domain = domain.replace("www.", "")
        # if domain.startswith("music."):
        #     domain = domain.replace("music.", "")
        # if domain.startswith("play."):
        #     domain = domain.replace("play.", "")
        top_domain = self.get_top_domain(domain)
        provider_name = ALL_PROVIDERS_MAPPING.get(top_domain)
        return provider_name

    @staticmethod
    def get_top_domain(domain: str) -> str:
        extracted = tldextract.extract(domain)
        # extracted.subdomain, extracted.domain, extracted.suffix
        if not extracted.domain or not extracted.suffix:
            return domain  # 无法解析则返回原值
        return f"{extracted.domain}.{extracted.suffix}"

    def is_supported_by_odesli(self, url: str) -> bool:
        """
        :param url:
        :return:
        """
        provider_name = self.get_provider_name(url)
        return provider_name in ODESLI_PROVIDERS


if __name__ == '__main__':
    import asyncio


    async def main():
        sp = SingParser()
        # r = await sp.parse("https://iheart.com/iheartradio")
        r = await sp.parse("https://music.apple.com/us/song/the-fate-of-ophelia/1833328840")
        # r = await sp.parse("https://music.apple.com/us/song/south-london-forever/1377117895")
        # r = await sp.parse("https://music.apple.com/us/song/%E9%80%9D%E5%8E%BB%E7%9A%84%E6%84%9B/203807523")
        # r = await sp.parse("https://music.apple.com/us/album/%E8%AA%B0%E6%98%8E%E6%B5%AA%E5%AD%90%E5%BF%83-%E7%B2%B5/203805635")
        # r = await sp.parse("https://music.amazon.com/albums/B009VLXMJA?marketplaceId=ATVPDKIKX0DER&musicTerritory=US&ref=dm_sh_mgrd8Tyly89kj8LRGFbXwIajk&trackAsin=B009VLXONY")
        # r = await sp.parse("https://music.amazon.com/albums/B003Y3ZTGA")
        # r = await sp.parse("https://audiomack.com/kweku-smoke/album/walk-with-me-7143177")
        # r = await sp.parse("https://audiomack.com/kweku-smoke/song/someday-soon-6600311")
        # r = await sp.parse("https://play.anghami.com/album/1055697102")
        # r = await sp.parse("https://play.anghami.com/song/1169343517")
        # r = await sp.parse("https://tidal.com/album/451505687/")
        # r = await sp.parse("https://tidal.com/album/451505687/track/451505707")
        # r = await sp.parse("https://tidal.com/track/451505689/u")
        # r = await sp.parse("https://www.joox.com/hk/album/QNUdai4hiD9AOdoWfzFdkw==")
        # r = await sp.parse("https://www.joox.com/hk/single/Eza4qbqXUipptWNX9Dmhow==")
        # r = await sp.parse("https://www.boomplay.com/albums/78926615")
        # r = await sp.parse("https://www.boomplay.com/songs/219911995")
        # r = await sp.parse("https://open.spotify.com/album/47OFnLtLVi5WrPYNXAwFGh")
        # r = await sp.parse("https://open.spotify.com/track/5JypFayfT1V5OG4xJ8q7jK")
        # r = await sp.parse("https://play.anghami.com/song/1235657379")
        # r = await sp.parse("https://play.anghami.com/album/1057425941")
        # r = await sp.parse("https://open.anghami.com/3HGBrn130Xb")
        # r = await sp.parse("https://www.deezer.com/us/album/623711221")
        # r = await sp.parse("https://www.deezer.com/us/track/3624611862")
        # r = await sp.parse("https://link.deezer.com/s/31tvHX4PmzIr3BXIjlCRm")
        # r = await sp.parse("https://music.youtube.com/playlist?list=OLAK5uy_kekq30oVNJRGIhjdEVYZbVEeyWyOT8jvY")
        # r = await sp.parse("https://music.youtube.com/watch?v=YheFCLnBmaY")
        # r = await sp.parse("https://www.pandora.com/artist/alan-jackson/everything-i-love/AL7jJJvf4792j7V")
        # r = await sp.parse("https://www.pandora.com/artist/alan-jackson/everything-i-love/little-bitty/TRzJjpKpKq5tcq9")
        # r = await sp.parse("https://soundcloud.com/stbondmusic/bond-free-ft-cuppy?in=soundcloud/sets/i-am-other-vol-2")
        # r = await sp.parse("https://soundcloud.com/malfunction-disfunction/annie-hill-ethos-original-mix?utm_source=clipboard&utm_medium=text&utm_campaign=social_sharing")
        # r = await sp.parse("https://soundcloud.com/soundcloud/sets/i-am-other-vol-2")
        # r = await sp.parse("https://theprotomen.bandcamp.com/album/act-iii-this-city-made-us")
        # r = await sp.parse("https://theprotomen.bandcamp.com/track/the-calm")
        # r = await sp.parse("https://music.yandex.com/album/38887997")
        # r = await sp.parse("https://music.yandex.com/album/38887997/track/144498905")
        print(r)


    asyncio.run(main())
