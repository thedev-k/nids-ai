import math
from typing import Optional, Any, Dict
from pydantic import BaseModel, Field, field_validator, ConfigDict


class NetworkFlow(BaseModel):
    """
    Pydantic schema for network flow records.
    Directly satisfies PRD Section 3.4.
    """
    model_config = ConfigDict(extra="allow", populate_by_name=True)

    flow_id: Optional[str] = None
    destination_port: int = Field(0, ge=0, le=65535)
    flow_duration: int = Field(0, ge=0)
    total_fwd_packets: int = Field(0, ge=0)
    total_backward_packets: int = Field(0, ge=0)
    packet_length_mean: float = Field(0.0, ge=0)
    flow_bytes_s: float = Field(0.0)
    flow_packets_s: float = Field(0.0)
    label: str
    is_attack: int = Field(0, ge=0, le=1)

    @field_validator("flow_bytes_s", "flow_packets_s", mode="before")
    @classmethod
