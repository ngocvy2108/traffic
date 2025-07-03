from __future__ import annotations

from enum import Enum
from typing import List, Optional, Union
from datetime import datetime  # Thay thế AwareDatetime

from pydantic import (
    AnyUrl,
    BaseModel,
    Field,
    RootModel,
    confloat,
    constr,
)


class Address(BaseModel):
    addressCountry: Optional[str] = Field(None, description='The country. For example, Spain')
    addressLocality: Optional[str] = Field(None, description='The locality in which the street address is, and which is in the region')
    addressRegion: Optional[str] = Field(None, description='The region in which the locality is, and which is in the country')
    district: Optional[str] = Field(None, description='A district is a type of administrative division that, in some countries, is managed by the local government')
    postOfficeBoxNumber: Optional[str] = Field(None, description='The post office box number for PO box addresses. For example, 03578')
    postalCode: Optional[str] = Field(None, description='The postal code. For example, 24004')
    streetAddress: Optional[str] = Field(None, description='The street address')
    streetNr: Optional[str] = Field(None, description='Number identifying a specific property on a public street')


class LaneDirection(Enum):
    forward = 'forward'
    backward = 'backward'


class Type(Enum):
    Point = 'Point'


class Location(BaseModel):
    bbox: Optional[List[float]] = Field(None, min_length=4)
    coordinates: List[float] = Field(..., min_length=2)
    type: Type


class Coordinate(RootModel[List[float]]):
    root: List[float]


class Type1(Enum):
    LineString = 'LineString'


class Location1(BaseModel):
    bbox: Optional[List[float]] = Field(None, min_length=4)
    coordinates: List[Coordinate] = Field(..., min_length=2)
    type: Type1


class Type2(Enum):
    Polygon = 'Polygon'


class Location2(BaseModel):
    bbox: Optional[List[float]] = Field(None, min_length=4)
    coordinates: List[List[Coordinate]]
    type: Type2


class Type3(Enum):
    MultiPoint = 'MultiPoint'


class Location3(BaseModel):
    bbox: Optional[List[float]] = Field(None, min_length=4)
    coordinates: List[List[float]]
    type: Type3


class Type4(Enum):
    MultiLineString = 'MultiLineString'


class Location4(BaseModel):
    bbox: Optional[List[float]] = Field(None, min_length=4)
    coordinates: List[List[Coordinate]]
    type: Type4


class Type5(Enum):
    MultiPolygon = 'MultiPolygon'


class Location5(BaseModel):
    bbox: Optional[List[float]] = Field(None, min_length=4)
    coordinates: List[List[List[Coordinate]]]
    type: Type5


class Type6(Enum):
    TrafficFlowObserved = 'TrafficFlowObserved'


class VehicleType(Enum):
    agriculturalVehicle = 'agriculturalVehicle'
    bicycle = 'bicycle'
    bus = 'bus'
    minibus = 'minibus'
    car = 'car'
    caravan = 'caravan'
    tram = 'tram'
    tanker = 'tanker'
    carWithCaravan = 'carWithCaravan'
    carWithTrailer = 'carWithTrailer'
    lorry = 'lorry'
    moped = 'moped'
    motorcycle = 'motorcycle'
    motorcycleWithSideCar = 'motorcycleWithSideCar'
    motorscooter = 'motorscooter'
    trailer = 'trailer'
    van = 'van'
    constructionOrMaintenanceVehicle = 'constructionOrMaintenanceVehicle'
    trolley = 'trolley'
    binTrolley = 'binTrolley'
    sweepingMachine = 'sweepingMachine'
    cleaningTrolley = 'cleaningTrolley'


class TrafficFlowObserved(BaseModel):
    address: Optional[Address] = Field(None, description='The mailing address')
    alternateName: Optional[str] = Field(None, description='An alternative name for this item')
    areaServed: Optional[str] = Field(None, description='The geographic area where a service or offered item is provided')
    averageGapDistance: Optional[confloat(ge=0.0)] = Field(None, description='Average gap distance between consecutive vehicles')
    averageHeadwayTime: Optional[confloat(ge=0.0)] = Field(None, description='Average headway time')
    averageVehicleLength: Optional[confloat(ge=0.0)] = Field(None, description='Average length of the vehicles')
    averageVehicleSpeed: Optional[confloat(ge=0.0)] = Field(None, description='Average speed of the vehicles')
    congested: Optional[bool] = Field(None, description='Flags whether there was a traffic congestion during the observation period')
    dataProvider: Optional[str] = Field(None, description='Provider of the harmonised data entity')
    dateCreated: Optional[datetime] = Field(None, description='Entity creation timestamp')
    dateModified: Optional[datetime] = Field(None, description='Last modification timestamp')
    dateObserved: Optional[str] = Field(None, description='The date and time of this observation in ISO8601 UTC format')
    dateObservedFrom: Optional[datetime] = Field(None, description='Observation period start date and time')
    dateObservedTo: Optional[datetime] = Field(None, description='Observation period end date and time')
    description: Optional[str] = Field(None, description='A description of this item')
    id: Optional[Union[constr(pattern=r'^[\w\-\.{}$\+\*\[\]|~^@!, :\\]+$', min_length=1, max_length=256), AnyUrl]] = Field(None, description='Unique identifier')
    intensity: Optional[confloat(ge=0.0)] = Field(None, description='Total number of vehicles detected')
    laneDirection: Optional[LaneDirection] = Field(None, description='Usual direction of travel in the lane')
    laneId: Optional[confloat(ge=1.0)] = Field(None, description='Lane identifier')
    location: Optional[Union[Location, Location1, Location2, Location3, Location4, Location5]] = Field(None, description='Geojson reference')
    name: Optional[str] = Field(None, description='The name of this item')
    occupancy: Optional[confloat(ge=0.0, le=1.0)] = Field(None, description='Fraction of the observation time with vehicle occupying')
    owner: Optional[List[Union[constr(pattern=r'^[\w\-\.{}$\+\*\[\]|~^@!,:\\]+$', min_length=1, max_length=256), AnyUrl]]] = Field(None, description='List of owner ids')
    refRoadSegment: Optional[AnyUrl] = Field(None, description='Reference to RoadSegment')
    reversedLane: Optional[bool] = Field(None, description='Flags whether traffic in the lane was reversed')
    seeAlso: Optional[Union[List[AnyUrl], AnyUrl]] = Field(None, description='Additional resources')
    source: Optional[str] = Field(None, description='Original data source')
    type: Optional[Type6] = Field(None, description='Entity type')
    vehicleSubType: Optional[str] = Field(None, description='Sub type of vehicle')
    vehicleType: Optional[VehicleType] = Field(None, description='Type of vehicle')
