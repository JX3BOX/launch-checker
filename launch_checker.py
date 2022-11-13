import asyncio
from contextlib import closing, suppress
from typing import Any, Dict
from urllib.request import urlopen

from fastapi import FastAPI

app = FastAPI()

servers = []
server_map = {}


async def check(host: str, port: str, *, timeout: int = 3) -> None:
    async def socket_connector(host: str, port: str, timeout: int = 3) -> bool:
        with suppress(Exception):
            _, w = await asyncio.wait_for(
                asyncio.open_connection(host, port), timeout=timeout
            )
            w.close()
            return True
        return False

    while True:
        if await socket_connector(host=host, port=port, timeout=timeout):
            server_map[(host, port)] = True
            await asyncio.sleep(60)
            continue

        server_map[(host, port)] = False

        while True:
            if await socket_connector(host=host, port=port, timeout=timeout):
                server_map[(host, port)] = True
                break


async def main() -> None:
    with closing(
        urlopen(
            "http://jx3comm.xoyocdn.com"
            "/jx3hd/zhcn_hd/serverlist/serverlist.ini"
        )
    ) as resp:
        for lines in resp.readlines():
            line = lines.decode("gbk").split("\t")
            servers.append(
                {
                    "zoneName": line[11],
                    "server": line[1],
                    "ipAddress": line[3],
                    "ipPort": line[4],
                    "mainServer": line[10],
                }
            )
            server_map[(line[3], line[4])] = False

    with closing(
        urlopen(
            "http://jx3clc-autoupdate.xoyocdn.com"
            "/jx3classic_v4/classic_yq/serverlist/serverlist.ini"
        )
    ) as resp:
        for lines in resp.readlines():
            line = lines.decode("gbk").split("\t")
            servers.append(
                {
                    "zoneName": line[11],
                    "serverName": line[1],
                    "ipAddress": line[3],
                    "ipPort": line[4],
                    "mainServer": line[10],
                }
            )
            server_map[(line[3], line[4])] = False

    with closing(
        urlopen(
            "http://jx3clc-autoupdate.xoyocdn.com"
            "/jx3classic_v4/classic_yq/serverlist/serverlist.ini"
        )
    ) as resp:
        for lines in resp.readlines():
            line = lines.decode("gbk").split("\t")
            servers.append(
                {
                    "zoneName": "國際服",
                    "server": line[1],
                    "ipAddress": line[3],
                    "ipPort": line[4],
                    "mainServer": line[1],
                }
            )
            server_map[(line[3], line[4])] = False

    await asyncio.gather(
        *[check(host=server[0], port=server[1]) for server in server_map]
    )


@app.on_event("startup")
async def startup():
    asyncio.create_task(main())


@app.get("/")
async def launch() -> Dict[str, Any]:
    return {
        "code": 0,
        "msg": "success",
        "tag": "GetZoneInfo",
        "data": [
            server
            | {
                "connectState": server_map[
                    (server["ipAddress"], server["ipPort"])
                ]
            }
            for server in servers
        ],
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("launch_checker:app", host="0.0.0.0", port=11003)
