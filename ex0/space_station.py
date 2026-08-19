from pydantic import BaseModel, Field, ValidationError
from datetime import datetime


class SpaceStation(BaseModel):
    station_id: str = Field(min_length=3, max_length=10)
    name: str = Field(min_length=1, max_length=50)
    crew_size: int = Field(ge=1, le=20)
    power_level: float = Field(ge=0.0, le=100.0)
    oxygen_level: float = Field(ge=0.0, le=100.0)
    last_maintenance: datetime
    is_operational: bool = True
    notes: str | None = Field(default=None, max_length=200)


def main() -> None:
    print("\nSpace Station Data Validation\n"
          "========================================\n"
          "Valid station created:")
    try:
        station_data = SpaceStation(
            station_id="ISS001",
            name="International Space Station",
            crew_size=6,
            power_level=85.5,
            oxygen_level=92.3,
            last_maintenance=datetime.fromisoformat("2026-08-10T12:00:00"),
        )

        print(f"ID: {station_data.station_id}\n"
              f"Name: {station_data.name}\n"
              f"Crew: {station_data.crew_size} people\n"
              f"Power: {station_data.power_level}%\n"
              f"Oxygen: {station_data.oxygen_level}%")
        if station_data.is_operational is True:
            print("Status: Operational")

    except ValidationError as e:
        print(e.errors()[0]["msg"])

    print("\n========================================\n"
          "Expected validation error:")
    try:
        station_data = SpaceStation(
                station_id="ISS001",
                name="International Space Station",
                crew_size=25,
                power_level=85.5,
                oxygen_level=92.3,
                last_maintenance=datetime.fromisoformat("2026-08-10T12:00:00"),
            )
    except ValidationError as e:
        print(e.errors()[0]["msg"])


if __name__ == "__main__":
    main()
