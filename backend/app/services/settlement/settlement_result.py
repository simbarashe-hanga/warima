from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class SettlementExecutionStatus(str, Enum):
    """
    Result status returned by a settlement handler.
    """

    COMPLETED = "COMPLETED"
    PROCESSING = "PROCESSING"
    FAILED = "FAILED"


@dataclass
class SettlementResult:
    """
    Standard result returned by settlement handlers.

    This object describes what happened during settlement
    execution. It does not commit database transactions.
    """

    status: SettlementExecutionStatus

    settlement_id: str | None = None

    external_reference: str | None = None

    error: str | None = None

    metadata: dict[str, Any] = field(
        default_factory=dict
    )

    @property
    def succeeded(self) -> bool:
        return (
            self.status
            == SettlementExecutionStatus.COMPLETED
        )

    @property
    def failed(self) -> bool:
        return (
            self.status
            == SettlementExecutionStatus.FAILED
        )

    @property
    def processing(self) -> bool:
        return (
            self.status
            == SettlementExecutionStatus.PROCESSING
        )
