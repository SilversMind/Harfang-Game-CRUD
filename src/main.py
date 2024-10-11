from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from src.constants import LOGGER_NAME
from src.core.router import game_router
from src.core.database import engine, Base

import logging

logger = logging.getLogger(LOGGER_NAME)
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)


Base.metadata.create_all(bind=engine)
logger.info("Starting HarfangLab server application...")
app = FastAPI()
app.include_router(game_router, prefix="/games")

""" @app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc):
    return JSONResponse(
        status_code=400,
        content={"message": "Invalid parameters provided. Please refer to the documentation to "
                 "check the expected parameters"},
    ) """
