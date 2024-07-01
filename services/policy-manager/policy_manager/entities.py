from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID, uuid4


@dataclass
class Policy:
    id: int
    statements: str


@dataclass
class Data:
    data_collected_date: datetime = datetime.now()
    last_maintenance_date: datetime = datetime.now()
    location: str = "unknown"
    sustainability_index: float = -1.0
    total_energy_consumption: float = -1.0
    peak_energy_consumption: float = -1.0
    off_peak_energy_consumption: float = -1.0
    energy_consumption_per_hour: float = -1.0
    renewable_energy_consumption: float = -1.0
    non_renewable_energy_consumption: float = -1.0
    co2_emissions: float = -1.0
    renewable_energy_percentage: float = -1.0
    uptime: float = -1.0
    downtime: float = -1.0
    maintenance_frequency: float = -1.0
    energy_efficiency_rating: float = -1.0
    carbon_footprint_reduction: float = -1.0
    id: UUID = field(default_factory=uuid4)


@dataclass
class Hop:
    isd_as: str
    collected_data: list[Data]


@dataclass
class Path:
    fingerprint: str
    hops: list[Hop]
