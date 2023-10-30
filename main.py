from src.server.logs.index import Logger
from src.server.routes.index import Routes
logger = Logger('HVK - WEB SOCKET')



app = Routes().starting()