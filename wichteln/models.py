from pydantic import BaseModel, Field, field_validator

class Participant(BaseModel):
    name: str = Field(..., description='The name of the participant')
    email: str | None = Field(None, description='The email address of the participant')


class Participants(BaseModel):
    participants: list[Participant] = Field(..., min_length=2, description='List of participants')

    @field_validator('participants')
    @classmethod
    def participants_must_be_unique(cls, participants: list[Participant]) -> list[Participant]:
        if len({participant.name for participant in participants}) != len(participants):
            raise ValueError('Participants must be unique')
        return participants


class Constraint(BaseModel):
    giver: str = Field(..., description='The name of the participant')
    forbidden: list[str] = Field(..., description='List of participants that the participant cannot draw')


class Constraints(BaseModel):
    constraints: list[Constraint] = Field(..., description='List of constraints')


class EmailConfig(BaseModel):
    pass


class Config(BaseModel):
    participants: list[Participant] = Field(..., min_length=2, description='List of participants')
    constraints: list[Constraint] = Field(default_factory=list, description='List of constraints')
    email_config: EmailConfig = Field(default_factory=EmailConfig, description='Email configuration')

    @field_validator('participants')
    @classmethod
    def participants_must_be_unique(cls, participants: list[Participant]) -> list[Participant]:
        if len({participant.name for participant in participants}) != len(participants):
            raise ValueError('Participants must be unique')
        return participants
