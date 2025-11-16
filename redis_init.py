from redis.asyncio import Redis, ConnectionPool

pool = ConnectionPool(host='localhost', port=6379, db=0)

async def get_redis():
    redis = Redis(connection_pool=pool)
    return redis