from abc import ABC
from dataclasses import dataclass, fields
from datetime import datetime

from policy_manager.entities import Data, Hop, Path


@dataclass
class HoppipollaSymbol(ABC):
    pass


@dataclass
class PathSymbol(HoppipollaSymbol):
    path: Path

    def __repr__(self) -> str:
        return f"path(\"{self.path.fingerprint}\")."


@dataclass
class HopSymbol(HoppipollaSymbol):
    hop: Hop

    def __repr__(self) -> str:
        return f"hop(\"{self.hop.isd_as}\")."


@dataclass
class DataSymbol(HoppipollaSymbol):
    data: Data

    def __repr__(self) -> str:
        out = f"data(\"{self.data.id}\")."
        for f in fields(Data):
            name = f.name

            if name == "id":
                continue

            value = getattr(self.data, name)

            if isinstance(value, datetime):
                out += f"\n{name}(\"{self.data.id}\", {
                    int(value.timestamp() * 1000)})."
            elif type(value) is int:
                out += f"\n{name}(\"{self.data.id}\", {value})."
            else:
                out += f"\n{name}(\"{self.data.id}\", \"{value}\")."

        return out


@dataclass
class ContainsSymbol(HoppipollaSymbol):
    path: Path
    hop: Hop

    def __repr__(self) -> str:
        return f"contains(\"{self.path.fingerprint}\", \"{self.hop.isd_as}\")."


@dataclass
class CollectedSymbol(HoppipollaSymbol):
    hop: Hop
    data: Data

    def __repr__(self) -> str:
        return f"collected(\"{self.hop.isd_as}\", \"{self.data.id}\")."
