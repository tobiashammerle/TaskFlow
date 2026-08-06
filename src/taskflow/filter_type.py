from enum import Enum

class FilterType(Enum):
    ALL = "all"

    COMPLETED = "completed"
    OPEN = "open"

    HIGH_PRIORITY = "high_priority"
    MEDIUM_PRIORITY = "medium_priority"
    LOW_PRIORITY = "low_priority"

    WITH_DUE_DATE = "with_due_date"
    WITHOUT_DUE_DATE = "without_due_dat"

