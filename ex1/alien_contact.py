from pydantic import BaseModel, model_validator, Field, ValidationError
from enum import Enum
from datetime import datetime


class ContactType(str, Enum):
    RADIO = "radio"
    VISUAL = "visual"
    PHYSICAL = "physical"
    TELEPATHIC = "telepathic"


class AlienContact(BaseModel):
    contact_id: str = Field(min_length=5, max_length=15,
                            description="5-15 characters")
    timestamp: datetime
    location: str = Field(min_length=3, max_length=100,
                          description="3-100 characters")
    contact_type: ContactType
    signal_strength: float = Field(ge=0.0, le=10.0, description="0-10 scale")
    duration_minutes: int = Field(ge=1, le=1440,
                                  description="max 24 hours")
    witness_count: int = Field(ge=1, le=100,
                               description="1-100 people")
    message_received: str | None = Field(default=None, max_length=500,
                                         description="max 500 characters")
    is_verified: bool = False

    @model_validator(mode="after")
    def validate_contact(self) -> "AlienContact":
        if not self.contact_id.startswith("AC"):
            raise ValueError("Contact ID must start with 'AC' (Alien Contact)")
        if (self.contact_type is ContactType.PHYSICAL
                and not self.is_verified):
            raise ValueError("Physical contact reports must be verified")
        if (self.contact_type is ContactType.TELEPATHIC
                and self.witness_count < 3):
            raise ValueError("Telepathic contact requires at least 3 "
                             "witnesses")
        if self.signal_strength > 7.0 and not self.message_received:
            raise ValueError("Strong signals (> 7.0) should include received "
                             "messages")
        return self


def main() -> None:
    print("\nAlien Contact Log Validation\n"
          "======================================\n"
          "Valid contact report:")
    try:
        valid_contact = AlienContact(
            contact_id="AC_2024_001",
            timestamp=datetime.fromisoformat("2026-08-10T12:00:00"),
            location="Area 51, Nevada",
            contact_type=ContactType.RADIO,
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=5,
            message_received="Greetings from Zeta Reticuli"
        )
        print(f"ID: {valid_contact.contact_id}")
        print(f"Type: {valid_contact.contact_type.value}")
        print(f"Location: {valid_contact.location}")
        print(f"Signal: {valid_contact.signal_strength}/10")
        print(f"Duration: {valid_contact.duration_minutes}")
        print(f"Witnesses: {valid_contact.witness_count}")
        print(f"Message: '{valid_contact.message_received}'")

    except ValidationError as e:
        print(e.errors()[0]["msg"])

    print("\n======================================\n"
          "Expected validation error:")
    try:
        invalid_contact = AlienContact(
            contact_id="AC_2024_001",
            timestamp=datetime.fromisoformat("2026-08-10T12:00:00"),
            location="Area 51, Nevada",
            contact_type=ContactType.TELEPATHIC,
            signal_strength=8.5,
            duration_minutes=45,
            witness_count=2,
            message_received="Greetings from Zeta Reticuli"
        )
        print(f"ID: {invalid_contact.contact_id}")
        print(f"Type: {invalid_contact.contact_type.value}")
        print(f"Location: {invalid_contact.location}")
        print(f"Signal: {invalid_contact.signal_strength}/10")
        print(f"Duration: {invalid_contact.duration_minutes}")
        print(f"Witnesses: {invalid_contact.witness_count}")
        print(f"Message: '{invalid_contact.message_received}'")

    except ValidationError as e:
        print(e.errors()[0]["msg"])


if __name__ == "__main__":
    main()
