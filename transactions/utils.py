import uuid
import random


def generate_transaction_ref_code():
    # Generate a unique ID using the uuid module
    ref_code = uuid.uuid4()
    ref_code = 'lyntm-' + str(ref_code)

    # Convert the unique ID to a string and return it
    return ref_code


def generate_service_id():
    service_id = random.randint(10000000000, 99999999999)
    return str(service_id)
