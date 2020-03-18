#!/usr/bin/env python3
# -*- coding: utf-8 -*-

'''
Streams allow sending and receiving data without using 
callbacks or low-level protocols and transports
'''
import asyncio
import multiprocessing
import time


async def _handler_func(reader, writer):
    data = await reader.read(100)
    message = data.decode()
    addr = writer.get_extra_info('peername')
    print(f"Server recv from {addr!r}: {message!r}")

    print(f"Server send: {message!r}")
    writer.write(data)
    await writer.drain()
    writer.close()
    await writer.wait_closed()
async def tcp_echo_server():
    '''
    easy server
    '''
    server = await asyncio.start_server(_handler_func, host="0.0.0.0", port=9000)
    
    addr = server.sockets[0].getsockname()
    print(f'Server on: {addr}')
    
    async with server:
        await server.serve_forever()
        
    
async def tcp_echo_client(message):
    '''
    easy client
    '''
    reader, writer = await asyncio.open_connection('127.0.0.1', 9000)

    print(f'Client send: {message!r}')
    writer.write(message.encode())
    await writer.drain()

    data = await reader.read(100)
    print(f'Client rece: {data.decode()!r}')

    writer.close()
    await writer.wait_closed()
def tcp_echo_client_main():
    time.sleep(3)
    asyncio.run(tcp_echo_client('Hello World!'))
    

if __name__ == "__main__":
    ###start client
    client = multiprocessing.Process(target=tcp_echo_client_main)
    client.start()
    
    ###start server
    asyncio.run(tcp_echo_server())

    ###free client
    client.join()
