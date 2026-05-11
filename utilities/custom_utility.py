import random
import time

def generate_unique_email(base_email):
    random_number = random.randint(10000,99999)
    name, domain = str(base_email).split("@")
    return f"{name}_{random_number}@{domain}"
    # return f"{name}_{int(time.time())}_{random.randint(100,999)}@{domain}"