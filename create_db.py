from impactour_database import Base,engine
from impactour_models import Domain_Class
print("creating DB")

Base.metadata.create_all(engine)