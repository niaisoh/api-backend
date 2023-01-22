import asyncio
from aio_pika import connect_robust
from aio_pika.patterns import RPC
from settings import rabbitmq
from func import get


async def ecof_rpc_robust(worker=1):
    connection = await connect_robust(
        "amqp://{}:{}@{}/".format(rabbitmq.get('user'), rabbitmq.get('pass'), rabbitmq.get('host')), client_properties={"connection_name": "callee"},)
    # Creating channel
    work_ch = []
    work_q = []
    for i in range(worker):
        print("worker {} register".format(i))
        work_ch.append(await connection.channel())
        work_q.append(await RPC.create(work_ch[i]))
        await work_q[i].register("data_get", get, auto_delete=True)
    return connection

def ecof_rpc_robust_main(worker=3):
    loop = asyncio.new_event_loop()
    connection = loop.run_until_complete(ecof_rpc_robust(worker=worker))
    try:
        print("[x] Awaiting RPC requests")
        loop.run_forever()
    finally:
        loop.run_until_complete(connection.close())
        loop.shutdown_asyncgens()
        print("Shutdown RPC requests")

if __name__ == "__main__":
    ecof_rpc_robust_main()