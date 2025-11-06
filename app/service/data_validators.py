from fastapi import HTTPException


async def unique_check(data, data_entity: str):
    if data is not None:
        return data
    else:
        raise HTTPException(401, detail=f"{data_entity} with such name already exists")


async def permission_check(role: str, acceptable_roles: tuple):
    if role in acceptable_roles:
        pass
    else:
        raise HTTPException(403, detail="Permission denied")


async def existing_check(data, data_entity: str):
    if data is not None:
        return data
    else:
        raise HTTPException(401, detail=f"Such {data_entity} does not exist")