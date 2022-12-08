import aiohttp
import asyncio
from bs4 import BeautifulSoup

URL = 'https://free-proxy-list.net/'
TASKS = []

async def get_proxies(count=None) -> list: #[0.0.0.0, 127.0.1.1, 192.168.0.1]
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as response:
            html = await response.text()
            soup = BeautifulSoup(html, 'html.parser')
            textarea = soup.find('textarea').text
            proxies = []
            textarea = textarea.split('\n')
            for index, line in enumerate(textarea):
                if not index in range(0, 3):
                    proxies.append(line)
    return proxies if count is None else proxies[:count]

async def check_proxy(_proxy:str, output:list):
    try:
        session = aiohttp.ClientSession()
        resp = await session.get('https://httpbin.org/ip', proxy=f'http://{_proxy}', timeout=4)
        if resp.status == 200:
            print('Ok')
            output.append(_proxy)
    except Exception as ex:
        pass
    finally:
        await session.close()

async def save_result(result):

    with open('result.txt', 'w') as file:
        for proxy in result:
            file.write(proxy + '\n')


async def main():
    proxies = await get_proxies()
    result = []
    for proxy in proxies:
        TASKS.append(asyncio.ensure_future(check_proxy(proxy, result)))
    return result



if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(main())
    loop.run_until_complete(asyncio.wait(TASKS))
    loop.run_until_complete(save_result(result=result))
    loop.run_until_complete(asyncio.sleep(0.1))
    loop.close()