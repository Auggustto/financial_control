from fastapi import APIRouter
from starlette.responses import RedirectResponse

routers = APIRouter()

@routers.get('/', include_in_schema=False)
def check():
    return RedirectResponse(url="/docs")