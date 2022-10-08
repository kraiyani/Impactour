from sqlalchemy.sql.expression import null
from impactour_database import Base
from sqlalchemy import String, Boolean, Integer, Column, Text, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship

class Domain_Class(Base):

    __tablename__='domain'

    id = Column(Integer, nullable=False, primary_key=True)
    domain_code = Column(String(10), nullable=False)
    domain_name = Column(String(100), nullable=False)
    attribute_1 = Column(String(500), nullable=True)
    attribute_2 = Column(String(500), nullable=True)
    attribute_3 = Column(String(500), nullable=True)
    created_by = Column(Integer, nullable = False)
    created_date = Column(DateTime, nullable = False)
    modified_by = Column(Integer, nullable = True)
    modified_date = Column(DateTime, nullable = True)

    indicator_domins = relationship('Indicator_Class', backref='Domain_Class')
    domain_data_domains = relationship('Domain_data_Class', backref='Domain_Class')
    kpi_domains = relationship('KPI_Class', backref='Domain_Class')
    kpi_calculation_domains = relationship('KPI_calculation_Class', backref='Domain_Class')


class Pilot_Class(Base):

    __tablename__='pilot'

    id = Column(Integer, nullable=False, primary_key=True)
    pilot_code = Column(String(10), nullable=False)
    pilot_name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    country = Column(String(100), nullable=True)
    attribute_1 = Column(String(500), nullable=True)
    attribute_2 = Column(String(500), nullable=True)
    attribute_3 = Column(String(500), nullable=True)
    created_by = Column(Integer, nullable = False)
    created_date = Column(DateTime, nullable = False)
    modified_by = Column(Integer, nullable = True)
    modified_date = Column(DateTime, nullable = True)

    domain_data_pilots = relationship('Domain_data_Class', backref='Pilot_Class')
    kpi_calculation_pilots = relationship('KPI_calculation_Class', backref='Pilot_Class')


class Data_access_type_Class(Base):

    __tablename__='data_access_type'

    id = Column(Integer, nullable=False, primary_key=True)
    data_access_type_code = Column(String(10), nullable=False)
    data_access_type_name = Column(String(50), nullable=False)
    attribute_1 = Column(String(500), nullable=True)
    attribute_2 = Column(String(500), nullable=True)
    attribute_3 = Column(String(500), nullable=True)
    created_by = Column(Integer, nullable = False)
    created_date = Column(DateTime, nullable = False)
    modified_by = Column(Integer, nullable = True)
    modified_date = Column(DateTime, nullable = True)

    domain_data_data_access_types = relationship('Domain_data_Class', backref='Data_access_type_Class')


class Indicator_Class(Base):

    __tablename__='indicator'

    id = Column(Integer, nullable=False, primary_key=True)
    domain_id = Column(Integer, ForeignKey('domain.id'))
    criteria = Column(String(500), nullable=True)
    indicator_code = Column(String(50), nullable=False)
    indicator_name = Column(String(500), nullable=False)
    indicator_type = Column(String(100), nullable=True)
    update_periodicity = Column(String(50), nullable=True)
    unit = Column(String(500), nullable=False)
    attribute_1 = Column(String(500), nullable=True)
    attribute_2 = Column(String(500), nullable=True)
    attribute_3 = Column(String(500), nullable=True)
    created_by = Column(Integer, nullable = False)
    created_date = Column(DateTime, nullable = False)
    modified_by = Column(Integer, nullable = True)
    modified_date = Column(DateTime, nullable = True)

    domain_data_indicators = relationship('Domain_data_Class', backref='Indicator_Class')
    kpi_indicator_indicators = relationship('KPI_indicator_Class', backref='Indicator_Class')


class Data_type_Class(Base):

    __tablename__='data_type'

    id = Column(Integer, nullable=False, primary_key=True)
    data_type_code = Column(String(10), nullable=False)
    data_type_name = Column(String(50), nullable=False)
    attribute_1 = Column(String(500), nullable=True)
    attribute_2 = Column(String(500), nullable=True)
    attribute_3 = Column(String(500), nullable=True)
    created_by = Column(Integer, nullable = False)
    created_date = Column(DateTime, nullable = False)
    modified_by = Column(Integer, nullable = True)
    modified_date = Column(DateTime, nullable = True)

    domain_data_data_types = relationship('Domain_data_Class', backref='Data_type_Class')


class Domain_data_Class(Base):

    __tablename__='domain_data'

    id = Column(Integer, nullable=False, primary_key=True)
    domain_id = Column(Integer, ForeignKey("domain.id"))
    pilot_id = Column(Integer, ForeignKey("pilot.id"))
    data_access_type_id = Column(Integer, ForeignKey("data_access_type.id"))
    indicator_id = Column(Integer, ForeignKey("indicator.id"))
    data_type_id = Column(Integer, ForeignKey("data_type.id"))
    result = Column(Float, nullable = False)
    reference_time = Column(String(10), nullable=True)
    sources = Column(String(1000), nullable=True)
    remarks = Column(String(1000), nullable=True)
    attribute_1 = Column(String(500), nullable=True)
    attribute_2 = Column(String(500), nullable=True)
    attribute_3 = Column(String(500), nullable=True)
    created_by = Column(Integer, nullable = False)
    created_date = Column(DateTime, nullable = False)
    modified_by = Column(Integer, nullable = True)
    modified_date = Column(DateTime, nullable = True)


class KPI_Class(Base):

    __tablename__='kpi'

    id = Column(Integer, nullable=False, primary_key=True)
    domain_id = Column(Integer, ForeignKey("domain.id"))
    kpi_code = Column(String(50), nullable=False)
    kpi_name = Column(String(500), nullable=False)
    calculation_method = Column(String(1000), nullable=False)
    unit = Column(String(500), nullable=False)
    attribute_1 = Column(String(500), nullable=True)
    attribute_2 = Column(String(500), nullable=True)
    attribute_3 = Column(String(500), nullable=True)
    created_by = Column(Integer, nullable = False)
    created_date = Column(DateTime, nullable = False)
    modified_by = Column(Integer, nullable = True)
    modified_date = Column(DateTime, nullable = True)

    kpi_calculation_kpis = relationship('KPI_calculation_Class', backref='KPI_Class')
    kpi_indicator_kpis = relationship('KPI_indicator_Class', backref='KPI_Class')


class KPI_calculation_Class(Base):

    __tablename__='kpi_calculation'

    id = Column(Integer, nullable=False, primary_key=True)
    domain_id = Column(Integer, ForeignKey("domain.id"))
    pilot_id = Column(Integer, ForeignKey("pilot.id"))
    kpi_id = Column(Integer, ForeignKey("kpi.id"))
    calculated_value = Column(Float, nullable = False)
    attribute_1 = Column(String(500), nullable=True)
    attribute_2 = Column(String(500), nullable=True)
    attribute_3 = Column(String(500), nullable=True)
    created_by = Column(Integer, nullable = False)
    created_date = Column(DateTime, nullable = False)
    modified_by = Column(Integer, nullable = True)
    modified_date = Column(DateTime, nullable = True)


class KPI_indicator_Class(Base):

    __tablename__='kpi_indicator'

    id = Column(Integer, nullable=False, primary_key=True)
    kpi_id = Column(Integer, ForeignKey("kpi.id"))
    indicator_id = Column(Integer, ForeignKey("indicator.id"))
    data_code = Column(String(10), nullable=True)
    attribute_1 = Column(String(500), nullable=True)
    attribute_2 = Column(String(500), nullable=True)
    attribute_3 = Column(String(500), nullable=True)
    created_by = Column(Integer, nullable = False)
    created_date = Column(DateTime, nullable = False)
    modified_by = Column(Integer, nullable = True)
    modified_date = Column(DateTime, nullable = True)