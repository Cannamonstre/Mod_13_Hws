import asyncio


async def start_strongman(name, power):
    print(f'Strongman {name} started the competition')

    for ball_num in range(1, 6):
        print(f'Strongman {name} lifted the ball number {ball_num}')
        await asyncio.sleep(1 / power)

    print(f'Strongman {name} finished the competition')


async def start_tournament():
    t1 = asyncio.create_task(start_strongman('Alexander', 3))
    t2 = asyncio.create_task(start_strongman('Joe', 4))
    t3 = asyncio.create_task(start_strongman('Edward', 5))

    await t1
    await t2
    await t3


asyncio.run(start_tournament())
