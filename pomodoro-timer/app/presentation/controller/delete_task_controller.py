from fastapi import Header


async def delete_task(id: str, userId: str = Header(None)):
    return
