from dotenv import load_dotenv
from app import create_app

load_dotenv(override=True)
app = create_app()