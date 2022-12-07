import uuid


def generate_transaction_ref_code():
    # Generate a unique ID using the uuid module
    ref_code = uuid.uuid4()
    ref_code = 'lyntm-' + str(ref_code)

    # Convert the unique ID to a string and return it
    return ref_code

