import logging
from fastapi import Request


logger = logging.getLogger(__name__) #создание объекта логера (__name__ соответствует текущему имени модуля)
logger.setLevel(logging.INFO) # устанавливает тип сообщений, которые будут логироваться (есть DEBUG-отладочная инфа, INFO-информ. сообщения, WARNING-предупр(умолч.), ERROR, CRITICAL)
handler = logging.FileHandler('info.log') #указываем, что логи будут в файле
handler.setLevel(logging.INFO) #какие сообщения будут записываться
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                              datefmt='%d-%m-%Y %H:%M:%S') #формат вывода логов
handler.setFormatter(formatter)
logger.addHandler(handler)


async def logging_middleware(request: Request, call_next):
    logger.info(f"Incoming request: {request.method} {request.url.path}") #записывает входящий запрос от юзера
    response = await call_next(request)
    logger.info(f"Outgoing response code: {response.status_code}") #записывает ответ юзеру
    return response