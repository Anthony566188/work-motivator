from starlette.middleware.cors import CORSMiddleware
from datetime import datetime
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Main(BaseModel):
    START_DATE: datetime
    END_DATE: datetime
    TOTAL_VALUE: float
    ACCUMULATED_VALUE: float


START_DATE = datetime(2026, 8, 24, 0, 0, 0)
END_DATE = datetime(2026, 9, 24, 0, 0, 0)
TOTAL_VALUE = 2300.00


def calculate_total_time() -> int:
    return int((END_DATE - START_DATE).total_seconds())


def rate_per_second() -> float:
    return TOTAL_VALUE / calculate_total_time()


def elapsed_time(date_now: datetime) -> int:
    return int((date_now - START_DATE).total_seconds())


@app.post("/")
def current_value(date_now: datetime):

    if date_now >= END_DATE:
        return TOTAL_VALUE

    main = Main(
        START_DATE=START_DATE,
        END_DATE=END_DATE,
        TOTAL_VALUE=TOTAL_VALUE,
        ACCUMULATED_VALUE=rate_per_second() * elapsed_time(date_now)
    )

    return main


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # Em produção local: ["http://localhost:3000"]
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)