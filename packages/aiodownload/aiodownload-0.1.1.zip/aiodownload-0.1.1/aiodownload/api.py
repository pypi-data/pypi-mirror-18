# -*- coding: utf-8 -*-

import asyncio
import aiohttp

from aiodownload import AioDownloadBundle, AioDownload


def swarm(urls):

    try:

        event_loop = asyncio.get_event_loop()
        client = aiohttp.ClientSession(loop=event_loop)
        download = AioDownload(client)
        for url in urls:
            bundle = AioDownloadBundle(url)
            download.priority_queue.put_nowait(
                (
                    bundle.priority,
                    bundle
                )
            )
        tasks = download.get_tasks(event_loop)
        event_loop.run_until_complete(asyncio.wait(tasks))

    finally:

        event_loop.close()


def one(url):

    swarm([url])
