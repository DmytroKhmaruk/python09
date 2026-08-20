from pydantic import BaseModel, model_validator, Field
from enum import Enum
from datetime import datetime


class ContractType(str, Enum):
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
    contact_type: ContractType
    signal_strength: float = Field(ge=0.0, le=10.0, description="0-10 scale")
    duration_minutes: int = Field(ge=1, le=1440,
                                  description="max 24 hours")
    witness_count: int = Field(ge=1, le=100,
                               description="1-100 people")
    message_received: str | None = Field(max_length=500,
                                         description="max 500 characters")
    is_verified: bool = False

    @model_validator(mode="after")
    def validate(self, ContactType):
        if not self.contact_id.startswith("AC"):
            raise ValueError("Contact ID must start with 'AC' (Alien Contact)")
        if (self.contact_type == ContactType.PHYSICAL
                and not self.is_verified):
            raise ValueError("Physical contact reports must be verified")
        if (self.contact_type == ContactType.TELEPATIC
                and self.witness_count < 3):
            raise ValueError("Telepathic contact requires at least 3"
                             "witnesses")
        if self.signal_strength > 7.0:
            raise ValueError("Strong signals (> 7.0) should include received"
                             "messages")
        return self
