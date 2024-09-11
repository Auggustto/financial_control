from fastapi import FastAPI

from app.routers.start import routers


app = FastAPI()

### include all routers ###
app.include_router(router=routers)