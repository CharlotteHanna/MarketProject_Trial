from enum import Enum


class ProductStatus(Enum):
    AVAILABLE = "available"
    RESERVED = "reserved"
    SOLD = "sold"




class PaymentStatus(Enum):
    IN_PROGRESS = "in_progress"
    DONE = "done"
    FAILED = "failed"