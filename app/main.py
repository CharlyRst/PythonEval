from fastapi import FastAPI, Body, HTTPException, Depends

from contextlib import asynccontextmanager

from pydantic import BaseModel, Field, ConfigDict
from typing import Literal

from app.db import SessionLocal, get_db, init_db
from app.stationdb import Station

from sqlalchemy import select
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

app = FastAPI(title="Dock Control", version="0.1.0")
init_db()

StationStatus = Literal["open", "closed", "maintenance"]

class StationCreate(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)

    code: str = Field(min_length=1)
    name: str = Field(min_length=1)
    capacity: int = Field(ge=1)
    status: StationStatus = "open"

class StationOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    code: str
    name: str
    capacity: int
    status: StationStatus

class StationPatch(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)
 
    name: str | None = Field(default=None, min_length=1)
    status: StationStatus | None = None

@app.get("/health")
def health() :
    return {"status" : "ok"}

# ------------- POST et GET de stations -------------

@app.post("/stations", status_code=201)
def post_stations(payload: StationCreate, db: Session = Depends(get_db)) -> StationOut :
    station = Station(**payload.model_dump())
    db.add(station)
    try :
        db.commit()
    except IntegrityError :
        db.rollback()
        raise HTTPException(status_code=409, detail=f"Le code {payload.code} existe déjà.")
    db.refresh(station)
    return station


@app.get("/stations")
def list_stations(status: StationStatus | None = None, db: Session = Depends(get_db)) -> list[StationOut]:
    station = select(Station)
    if status is not None:
        station = station.where(Station.status == status)
    return list(db.scalars(station).all())

# ------------- GET et PATCH de stations{id} -------------

@app.get("/stations/{station_id}")
def get_station(station_id: int, db: Session = Depends(get_db)) -> StationOut:
    row = db.get(Station, station_id)
    if row is None:
        raise HTTPException(status_code=404, detail="Station not found")
    return row

@app.patch("/stations/{station_id}", response_model=StationOut)
def update_station(station_id: int, payload: StationPatch, db: Session = Depends(get_db)):
    row = db.get(Station, station_id)
    if row is None:
        raise HTTPException(status_code=404, detail=f"La station {station_id} est introuvable.")
    if payload.name is not None:
        row.name = payload.name
    if payload.status is not None:
        row.status = payload.status
    db.commit()
    db.refresh(row)
    return row