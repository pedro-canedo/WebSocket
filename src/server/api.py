from fastapi import FastAPI, HTTPException, Request
from dotenv import load_dotenv
from src.server.middleware.index import MiddlewareApi

class Api:
    def __init__(self):
        load_dotenv()
        self.app = FastAPI(title="HVK-API", version="1.0.0")

        self._init_middleware()
        self.middleware = None

    def _init_middleware(self):
        self.middleware = MiddlewareApi(self.app)
        self.app = self.middleware.app
    
    def get_app(self):
        return self.app

    def origins_allowed(self):
        return MiddlewareApi(self.app).origins
    



app = Api().app

@app.middleware("http")
async def validate_origin(request: Request, call_next):
    allow = False
    origin = request.headers.get("origin")
    allow = True
    if not allow: 
        raise HTTPException(status_code=403, detail="Acesso negado ao domínio não permitido.")
    response = await call_next(request)
    return response
