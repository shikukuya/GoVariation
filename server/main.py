import asyncio
import random
import traceback as tb
import json
from websockets.server import serve, WebSocketServerProtocol
from websockets.exceptions import ConnectionClosedOK
from typing import *

"""
{
    "123456": {  # 房间号
        "players_n": 5,  # 下一个玩家的编号应该是什么
        "players": {  # 玩家
            "username": (2, "#000000"),
            "emanresu": (3, "#ffffff"),
            "nameuser": (4, "#ff0000"),
        },
        "options": {  # 游戏规则
            "width": 19,
            "height": 19,
            "hinder": "传统",
            "stone": 0,
            "firestone": 0
        },
        "game": [  # 棋盘
            [2, 3, 0],
            [2, 2, 0],
            [0, 3, 3]
        ]
    }
}
"""
data: Dict[str, Dict[str, Union[str, Dict[str, str], List[List[str]]]]] = {}


async def handler(ws: WebSocketServerProtocol, path):
    room = ""  # 房间号
    username = ""  # 用户名
    try:
        while True:
            dataR = (await ws.recv()).split()  # 收到的数据
            print(dataR)
            if len(dataR) == 3:  # <命令> <房间> <参数> or <命令> <游戏规则>
                if dataR[0] == "join":
                    if dataR[1] in data:  # 房间存在
                        # join <房间号> <用户名>
                        if dataR[2] in data[dataR[1]]["players"]:
                            await ws.send(json.dumps({
                                "msg": "上次未正确退出，请刷新页面或修改用户名"
                            }))
                        else:
                            # 把connection和username添加到data
                            room = dataR[1]
                            username = dataR[2]
                            data[dataR[1]]["players"][dataR[2]] = (
                                data[room]["players_n"],
                                f"#{random.randint(111111, 999999)}"
                            )
                            await ws.send(json.dumps({
                                "action": "update",
                                "game": data[room]["game"],
                                "players": data[room]["players"],
                                "options": data[room]["options"]
                            }))
                    else:
                        await ws.send(json.dumps({
                            "msg": "房间不存在"
                        }))
                if dataR[0] == "create":
                    # create <棋盘宽度> <棋盘高度> <碎石出现概率> <火石出现概率>
                    while True:
                        n = str(random.randint(100000, 999999))
                        if n == "114514":
                            n = "191981"
                        if n not in data:  # 防止房间号重复
                            data[n] = {
                                "players_n": 2,
                                "players": {},
                                "options": {
                                    "width": int(dataR[1]),
                                    "height": int(dataR[2])
                                },
                                "game": [
                                    [0 for _ in range(int(dataR[1]))]
                                    for _ in range(int(dataR[2]))
                                ]
                            }
                            await ws.send(json.dumps({
                                "msg": "创建成功，房间号：",
                                "input": n
                            }))
                            break
    except ConnectionClosedOK:
        if username and username in data[dataR[1]]["players"]:
            data[dataR[1]]["players"].pop(username)
    except Exception as e:
        tb.print_exc()

print("ws://0.0.0.0:34777/")
server = serve(handler, "0.0.0.0", 34777)
asyncio.get_event_loop().run_until_complete(server)
asyncio.get_event_loop().run_forever()
