from pydantic import BaseModel, model_validator, Field, ValidationError
from enum import Enum
from datetime import datetime


class Rank(str, Enum):
    COMMANDER = "commander"
    CAPTAIN = "captain"
    LIEUTENANT = "lieutenant"
    OFFICER = "officer"
    CADET = "cadet"


class CrewMember(BaseModel):
    member_id: str = Field(min_length=3, max_length=10,
                           description="3-10 characters")
    name: str = Field(min_length=2, max_length=50,
                      description="2-50 characters")
    rank: Rank
    age: int = Field(ge=18, le=80, description="18-80 years")
    specialization: str = Field(min_length=3, max_length=30,
                                description="3-30 characters")
    years_experience: int = Field(ge=0, le=50, description="0-50 years")
    is_active: bool = True


class SpaceMission(BaseModel):
    mission_id: str = Field(min_length=5, max_length=15,
                            description="5-15 characters")
    mission_name: str = Field(min_length=3, max_length=100,
                              description="3-100 characters")
    destination: str = Field(min_length=3, max_length=50,
                             description="3-50 characters")
    launch_date: datetime
    duration_days: int = Field(ge=1, le=3650,
                               description="1-3650 days max 10 years")
    crew: list[CrewMember] = Field(min_length=1, max_length=12,
                                   description="1-12 members")
    mission_status: str = Field(default="planned",
                                description="defaults to 'planned'")
    budget_millions: float = Field(ge=1.0, le=10000.0,
                                   description="1-10000 million dollars")

    @model_validator(mode="after")
    def validate_mission(self) -> "SpaceMission":
        if not self.mission_id.startswith("M"):
            raise ValueError("Mission ID must start with 'M'")

        has_leader = False
        for member in self.crew:
            if member.rank in (Rank.CAPTAIN, Rank.COMMANDER):
                has_leader = True
                break
        if not has_leader:
            raise ValueError(
                "Mission must have at least one Commander or Captain")

        experienced_count = 0
        for member in self.crew:
            if member.years_experience >= 5:
                experienced_count += 1
        if (self.duration_days > 365
                and experienced_count / len(self.crew) < 0.5):
            raise ValueError("Long missions (> 365 days) need 50% experienced "
                             "crew (5+ years)")
        for member in self.crew:
            if not member.is_active:
                raise ValueError("All crew members must be active")
        return self


def main() -> None:
    print("\nSpace Mission Crew Validation\n"
          "=========================================\n"
          "Valid mission created:")
    member1 = CrewMember(
        member_id="CM001",
        name="Sarah Connor",
        rank=Rank.COMMANDER,
        age=30,
        specialization="Mission Command",
        years_experience=5,
    )
    member2 = CrewMember(
        member_id="CM002",
        name="John Smith",
        rank=Rank.LIEUTENANT,
        age=27,
        specialization="Navigation",
        years_experience=2,
    )
    member3 = CrewMember(
        member_id="CM003",
        name="Alice Johnson",
        rank=Rank.OFFICER,
        age=25,
        specialization="Engineering",
        years_experience=5,
    )
    member4 = CrewMember(
        member_id="CM005",
        name="Alice Johnson",
        rank=Rank.CADET,
        age=25,
        specialization="Engineering",
        years_experience=0,
    )
    try:
        mission = SpaceMission(
            mission_name="Mars Colony Establishment",
            mission_id="M2024_MARS",
            destination="Mars",
            launch_date=datetime.fromisoformat("2026-08-10T12:00:00"),
            duration_days=900,
            budget_millions=2500.0,
            crew=[member1, member2, member3]
        )
        print(
            f"Mission: {mission.mission_name}\n"
            f"ID: {mission.mission_id}\n"
            f"Destination: {mission.destination}\n"
            f"Duration: {mission.duration_days} days\n"
            f"Budget: ${mission.budget_millions}M\n"
            f"Crew size: {len(mission.crew)}\n"
            f"Crew members:")
        for member in mission.crew:
            print(f"- {member.name} ({member.rank.value}) - "
                  f"{member.specialization}")
    except ValidationError as e:
        print(e.errors()[0]["msg"])

    print("\n=========================================\n"
          "Expected validation error:")
    try:
        mission = SpaceMission(
            mission_name="Mars Colony Establishment",
            mission_id="M2024_MARS",
            destination="Mars",
            launch_date=datetime.fromisoformat("2026-08-10T12:00:00"),
            duration_days=900,
            budget_millions=2500.0,
            crew=[member4, member2, member3]
        )
        print(
            f"Mission: {mission.mission_name}\n"
            f"ID: {mission.mission_id}\n"
            f"Destination: {mission.destination}\n"
            f"Duration: {mission.duration_days} days\n"
            f"Budget: ${mission.budget_millions}M\n"
            f"Crew size: {len(mission.crew)}\n"
            f"Crew members:")
        for member in mission.crew:
            print(f"- {member.name} ({member.rank.value}) - "
                  f"{member.specialization}")
    except ValidationError as e:
        print(e.errors()[0]["msg"])


if __name__ == "__main__":
    main()
