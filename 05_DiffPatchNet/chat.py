import asyncio
from cowsay import cowsay, list_cows
import shlex

clients = {}

free_names = list_cows()

async def chat(reader, writer):
    pipe = asyncio.Queue()
    reged = False
    me = ""
    send = asyncio.create_task(reader.readline())
    receive = asyncio.create_task(pipe.get())
    while not reader.at_eof():
        done, pending = await asyncio.wait([send, receive], return_when=asyncio.FIRST_COMPLETED)
        for q in done:
            if q is send:
                send = asyncio.create_task(reader.readline())
                line = shlex.split(q.result().decode().strip())
                if len(line) == 0:
                    continue
                if line[0] == 'cows':
                    cow_names = ' '.join(free_names) + '\n'
                    writer.write(f"Possible names: {cow_names}".encode())
                    await writer.drain()  
                elif line[0] == 'who':
                    res = "Users list: "
                    for cow in clients.keys():
                        res = res + cow + ' '
                    res = res + '\n'
                    writer.write(f"{res}".encode())
                    await writer.drain()  
                elif line[0] == 'login':
                    cow_name = line[1]
                    if reged:
                        writer.write("You are already reged!\n".encode())
                        await writer.drain()  
                    elif cow_name in clients.keys():
                        writer.write("This name is already busy!\n".encode())
                        await writer.drain()
                    elif cow_name not in free_names:
                        writer.write("Incorrect name!\n".encode())
                        await writer.drain()
                    else:
                        me = cow_name
                        free_names.remove(cow_name)
                        clients[me] = asyncio.Queue()
                        receive.cancel()
                        receive = asyncio.create_task(clients[me].get())
                        reged = True
                        writer.write(f"You are reged! Yot name is {me}\n".encode())
                        await writer.drain()
                elif line[0] == 'say':
                    if not reged:
                        writer.write(f"You need to be reged!\n".encode())
                        await writer.drain()
                    elif line[1] not in clients:
                        writer.write(f"User {line[1]} is not reged!\n".encode())
                        await writer.drain()
                    elif line[1] == me:
                        writer.write(f"Can't send message to yourself!\n".encode())
                        await writer.drain()
                    else:
                        await clients[line[1]].put(f"{cowsay(' '.join(line[2:]), cow = me)}")
                elif line[0] == 'yeild':
                    if not reged:
                        writer.write(f"You need to be reged!\n".encode())
                        await writer.drain()
                    else:
                        for out in clients.values():
                            if out is not clients[me]:
                                await out.put(f"{cowsay(' '.join(line[1:]), cow = me)}") 
                        writer.write("Message send!\n".encode())
                        await writer.drain()
                    
                elif line[0] == 'quit':
                    send.cancel()
                    receive.cancel()
                    if reged:
                        del clients[me]
                        free_names.append(me)
                    return
                else:
                    writer.write(f"Unknown command!".encode())
                    await writer.drain()
            elif q is receive:
                if reged:
                    receive = asyncio.create_task(clients[me].get())
                    writer.write(f"{q.result()}\n".encode())
                    await writer.drain()
                else:
                    receive = asyncio.create_task(pipe.get())
                    
    send.cancel()
    receive.cancel()
    print(me, "DONE")
    del clients[me]
    free_names.append(me)
    writer.close()
    await writer.wait_closed()

async def main():
    server = await asyncio.start_server(chat, '0.0.0.0', 1337)
    async with server:
        await server.serve_forever()

asyncio.run(main())


