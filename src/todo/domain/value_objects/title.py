from dataclasses import dataclass


@dataclass(frozen=True)
class Title:
  value: str

  def __post_init__(self):
    MAX_LENGTH = 100

    if not self.value:
      raise ValueError("Title cannot be empty")
    if len(self.value) > MAX_LENGTH:
      raise ValueError(f"Title cannot exceed {MAX_LENGTH} characters")
