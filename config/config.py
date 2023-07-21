from dotenv import load_dotenv
import os

load_dotenv()

def get_credentials():
    CLOUDMT_EMAIL = os.environ.get("CLOUDMT_EMAIL")
    CLOUDMT_PASSWORD = os.environ.get("CLOUDMT_PASSWORD")

    # Check environment variables exist
    if CLOUDMT_EMAIL is None:
        raise ValueError("Environment variable CLOUDMT_EMAIL not found")
    if CLOUDMT_PASSWORD is None:
        raise ValueError("Environment variable CLOUDMT_PASSWORD not found")
    
    return CLOUDMT_EMAIL, CLOUDMT_PASSWORD