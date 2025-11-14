from dataclasses import dataclass


@dataclass(frozen=True)
class Description:
  value: str

  def __post_init__(self):
    MAX_LENGTH = 500

    if not self.value:
      raise ValueError("Description cannot be empty")
    if len(self.value) > MAX_LENGTH:
      raise ValueError(f"Description cannot exceed {MAX_LENGTH} characters")
