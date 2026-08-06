from dataclasses import dataclass


@dataclass
class OnboardingResult:
    message: str
    completed: bool
    next_step: str | None
    save_session: bool = True
    create_wallets: bool = False
