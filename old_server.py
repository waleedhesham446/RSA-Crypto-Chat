#!/usr/bin/env python

import asyncio
import websockets
import json
import argparse
from utils import *

async def handleRequest(websocket):
    jsonData = await websocket.recv()
    data = json.loads(jsonData)
    if data['type'] == 'handshake':
        await websocket.send(json.dumps([e, n]))
    else:
        plaintext = decrypt(data['data'], d, n)
        print('Decrypted: ' + plaintext)
        await websocket.send('')

async def listen():
    async with websockets.serve(handleRequest, "localhost", listenning_port):
        await asyncio.Future()  # run forever

async def send():
    try:
        uri = "ws://localhost:" + sending_port
        async with websockets.connect(uri) as websocket:
            await websocket.send(json.dumps({ 'type': 'handshake' }))
            publicKey = await websocket.recv()
            _e, _n = json.loads(publicKey)
            
            while True:
                plaintext = input('Enter message: ')
                encrypted = encrypt(plaintext, _e, _n)
                async with websockets.connect(uri) as websocket:
                    await websocket.send(json.dumps({ 'type': 'data', 'data': encrypted }))
                    response = await websocket.recv()
                    print(response)
    except OSError:
        await asyncio.sleep(1)
        await send()

async def main():
    await asyncio.gather(
        listen(),
        send()
    )

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("-r", "--receive", required = True, help = "receive port")
    ap.add_argument("-s", "--send", required = True, help = "send port")
    args = vars(ap.parse_args())
    listenning_port = int(args["receive"])
    sending_port = args["send"]
    key_size = input('Enter key size: ')
    e, d, n = generate_key(key_size)
    asyncio.run(main())