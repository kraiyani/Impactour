from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine=create_engine("postgresql://postgres:admin@localhost:5432/impactour_api_table",echo=True)

# uri = "postgresql://mfdmxnmgqeaosv:1f32f7a10e1da655bf9d0db643f0a79b5927d14e3297c226f5f93d8981977d8c@ec2-99-81-68-240.eu-west-1.compute.amazonaws.com:5432/d2vkc6t5b403ol"
# engine=create_engine(uri)

Base=declarative_base()

SessionLocal=sessionmaker(bind=engine)