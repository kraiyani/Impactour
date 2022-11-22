from fastapi import FastAPI,status,HTTPException, UploadFile, File
from pydantic import BaseModel
from typing import Optional,List
from impactour_database import SessionLocal
import impactour_models
from datetime import datetime
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from sqlalchemy import and_ , func
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
from pandas import ExcelFile
import numpy as np
import os, tempfile

tags_metadata = [
    {
        "name": "Welcome",
        "description": "Happy reading document.",
    },
    {
        "name": "Domain_Table",
        "description": "A table where domain information is present.",
    },
    {
        "name": "Domain_Data_Table",
        "description": "A table where for each domain, pilot<-->indicator values are present.",
       
    },
    {
        "name": "KPI_Table",
        "description": "A table where KPI information is present.",
    },
    {
        "name": "KPI_calculation_Table",
        "description": "A table where domain and pilot wise, calculated KPI information is present.",
    },
    {
        "name": "Indicator_Table",
        "description": "A table where indicator information is present.",
    },
    {
        "name": "Pilot_Table",
        "description": "A table where pilot information is present.",
    },
    {
        "name": "KPI_Indicator_Table",
        "description": "A table where mapping of KPI and Indicator is present.",
    },
    {
        "name": "DSS_Filtering",
        "description": "A tables where you can find different Filtering criteria to feed the DSS modules.",
    },
    {
        "name": "DSS_Outcome",
        "description": "A tables where you can find different componenets of DSS modules.",
    },
]

description = """
Impactour API helps you to get Pilot data and lets you calculate KPIs... awesome stuff... 🚀

## Calls

Different tables have different Calls, and they are futher divided into different methods.

## Tecnalia

You will be able to:

* **Create, Read, Update, Delete**
"""

app = FastAPI(
    title="ImpactourAPI",
    description=description,
    version="0.0.1",
    terms_of_service="https://www.impactour.eu/",
    contact={
        "name": "João Francisco Alves Martins",
        "url": "https://www.dee.fct.unl.pt/equipa/professor-associado-com-agregacao/joao-francisco-alves-martins",
        "email": "jf.martins@fct.unl.pt",
    },
    openapi_tags=tags_metadata
    # license_info={
    #     "name": "Fastapi 0.85.0",
    #     "url": "https://fastapi.tiangolo.com/release-notes/",
    # },
)

origins = [
    "https://impactour.azurewebsites.net/","https://impactour.azurewebsites.net/*",
    "https://impactour.azurewebsites.net","*","https://localhost:9000","http://localhost",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Excel_domain_data_Class(BaseModel):
    domain_name: str
    pilot_name: str
    indicator_name: str
    data_privacy_name: str
    result : float
    reference_time : Optional[str] = ...
    sources : Optional[str] = ...
    remarks : Optional[str] = ...
    attribute_1 : Optional[str] = ...
    attribute_2 : Optional[str] = ...
    attribute_3 : Optional[str] = ...
    created_by : int
    created_date : datetime
    modified_by : Optional[int] = ...
    modified_date : Optional[datetime] = ...

    class Config:
        orm_mode=True

class Domain_Class(BaseModel): #serializer

    id : int
    domain_code : str
    domain_name : str
    attribute_1 : Optional[str] = ...
    attribute_2 : Optional[str] = ...
    attribute_3 : Optional[str] = ...
    created_by : int
    created_date : datetime
    modified_by : Optional[int] = ...
    modified_date : Optional[datetime] = ...

    class Config:
        orm_mode=True

class Domain_data_Class(BaseModel): #serializer
    id : int
    domain_id : int
    pilot_id : int
    data_access_type_id : int
    indicator_id : int
    data_type_id : int
    result : float
    reference_time : Optional[str] = ...
    sources : Optional[str] = ...
    remarks : Optional[str] = ...
    attribute_1 : Optional[str] = ...
    attribute_2 : Optional[str] = ...
    attribute_3 : Optional[str] = ...
    created_by : int
    created_date : datetime
    modified_by : Optional[int] = ...
    modified_date : Optional[datetime] = ...

    class Config:
        orm_mode=True

class KPI_Class(BaseModel):

    id : int
    domain_id : int
    kpi_code : str
    kpi_name : str
    calculation_method : str
    unit : str
    attribute_1 : Optional[str] = ...
    attribute_2 : Optional[str] = ...
    attribute_3 : Optional[str] = ...
    created_by : int
    created_date : datetime
    modified_by : Optional[int] = ...
    modified_date : Optional[datetime] = ...

    class Config:
        orm_mode=True

class KPI_calculation_Class(BaseModel):

    id : int
    domain_id : int
    pilot_id : int
    kpi_id : int
    calculated_value : float
    attribute_1 : Optional[str] = ...
    attribute_2 : Optional[str] = ...
    attribute_3 : Optional[str] = ...
    created_by : int
    created_date : datetime
    modified_by : Optional[int] = ...
    modified_date : Optional[datetime] = ...

    class Config:
        orm_mode=True

class Indicator_Class(BaseModel):

    id : int
    domain_id : int
    criteria : Optional[str] = ...
    indicator_code : str
    indicator_name : str
    indicator_type : Optional[str] = ...
    update_periodicity : Optional[str] = ...
    unit : str
    attribute_1 : Optional[str] = ...
    attribute_2 : Optional[str] = ...
    attribute_3 : Optional[str] = ...
    created_by : int
    created_date : datetime
    modified_by : Optional[int] = ...
    modified_date : Optional[datetime] = ...

    class Config:
        orm_mode=True

class Pilot_Class(BaseModel):

    id : int
    pilot_code : str
    pilot_name : str
    description : Optional[str] = ...
    country : Optional[str] = ...
    attribute_1 : Optional[str] = ...
    attribute_2 : Optional[str] = ...
    attribute_3 : Optional[str] = ...
    created_by : int
    created_date : datetime
    modified_by : Optional[int] = ...
    modified_date : Optional[datetime] = ...

    class Config:
        orm_mode=True

class KPI_indicator_Class(BaseModel):

    id : int
    kpi_id : int
    indicator_id : int
    data_code : Optional[str] = ...
    attribute_1 : Optional[str] = ...
    attribute_2 : Optional[str] = ...
    attribute_3 : Optional[str] = ...
    created_by : int
    created_date : datetime
    modified_by : Optional[int] = ...
    modified_date : Optional[datetime] = ...

    class Config:
        orm_mode=True

class Site_Class(BaseModel): #serializer

    id : int
    site_code : str
    site_name : str
    attribute_1 : Optional[str] = ...
    attribute_2 : Optional[str] = ...
    attribute_3 : Optional[str] = ...
    created_by : int
    created_date : datetime
    modified_by : Optional[int] = ...
    modified_date : Optional[datetime] = ...

    class Config:
        orm_mode=True


class Cultural_activity_Class(BaseModel): #serializer

    id : int
    activity_code : str
    activity_type : str
    attribute_1 : Optional[str] = ...
    attribute_2 : Optional[str] = ...
    attribute_3 : Optional[str] = ...
    created_by : int
    created_date : datetime
    modified_by : Optional[int] = ...
    modified_date : Optional[datetime] = ...

    class Config:
        orm_mode=True

class Cultural_tourism_impact_Class(BaseModel): #serializer

    id : int
    impact_code : str
    impact_option : str
    attribute_1 : Optional[str] = ...
    attribute_2 : Optional[str] = ...
    attribute_3 : Optional[str] = ...
    created_by : int
    created_date : datetime
    modified_by : Optional[int] = ...
    modified_date : Optional[datetime] = ...

    class Config:
        orm_mode=True

class Cultural_tourism_objective_Class(BaseModel): #serializer

    id : int
    objective_code : str
    objective_name : str
    attribute_1 : Optional[str] = ...
    attribute_2 : Optional[str] = ...
    attribute_3 : Optional[str] = ...
    created_by : int
    created_date : datetime
    modified_by : Optional[int] = ...
    modified_date : Optional[datetime] = ...

    class Config:
        orm_mode=True

class Strategy_Class(BaseModel): #serializer

    id : int
    strategy_code : str
    strategy_name : str
    strategy_value: str
    attribute_1 : Optional[str] = ...
    attribute_2 : Optional[str] = ...
    attribute_3 : Optional[str] = ...
    created_by : int
    created_date : datetime
    modified_by : Optional[int] = ...
    modified_date : Optional[datetime] = ...

    class Config:
        orm_mode=True


class Strategy_site_Class(BaseModel): #serializer

    id : int
    strategy_id : int
    site_id : int
    value: float
    attribute_1 : Optional[str] = ...
    attribute_2 : Optional[str] = ...
    attribute_3 : Optional[str] = ...
    created_by : int
    created_date : datetime
    modified_by : Optional[int] = ...
    modified_date : Optional[datetime] = ...

    class Config:
        orm_mode=True

class Strategy_cultural_activity_Class(BaseModel): #serializer

    id : int
    strategy_id : int
    cultural_activity_id : int
    value: float
    attribute_1 : Optional[str] = ...
    attribute_2 : Optional[str] = ...
    attribute_3 : Optional[str] = ...
    created_by : int
    created_date : datetime
    modified_by : Optional[int] = ...
    modified_date : Optional[datetime] = ...

    class Config:
        orm_mode=True

class Strategy_cultural_tourism_impact_Class(BaseModel): #serializer

    id : int
    strategy_id : int
    cultural_tourism_impact_id : int
    value: float
    attribute_1 : Optional[str] = ...
    attribute_2 : Optional[str] = ...
    attribute_3 : Optional[str] = ...
    created_by : int
    created_date : datetime
    modified_by : Optional[int] = ...
    modified_date : Optional[datetime] = ...

    class Config:
        orm_mode=True

class Strategy_cultural_tourism_objective_Class(BaseModel): #serializer

    id : int
    strategy_id : int
    cultural_tourism_objective_id : int
    value: float
    attribute_1 : Optional[str] = ...
    attribute_2 : Optional[str] = ...
    attribute_3 : Optional[str] = ...
    created_by : int
    created_date : datetime
    modified_by : Optional[int] = ...
    modified_date : Optional[datetime] = ...

    class Config:
        orm_mode=True

class Strategy_domain_Class(BaseModel): #serializer

    id : int
    strategy_id : int
    domain_id : int
    value: float
    attribute_1 : Optional[str] = ...
    attribute_2 : Optional[str] = ...
    attribute_3 : Optional[str] = ...
    created_by : int
    created_date : datetime
    modified_by : Optional[int] = ...
    modified_date : Optional[datetime] = ...

    class Config:
        orm_mode=True

class Action_Class(BaseModel): #serializer

    id : int
    strategy_id : int
    action_name : str
    action_code: str
    attribute_1 : Optional[str] = ...
    attribute_2 : Optional[str] = ...
    attribute_3 : Optional[str] = ...
    created_by : int
    created_date : datetime
    modified_by : Optional[int] = ...
    modified_date : Optional[datetime] = ...

    class Config:
        orm_mode=True

class Action_kpi_Class(BaseModel): #serializer

    id : int
    action_id : int
    kpi_id : int
    value: float
    attribute_1 : Optional[str] = ...
    attribute_2 : Optional[str] = ...
    attribute_3 : Optional[str] = ...
    created_by : int
    created_date : datetime
    modified_by : Optional[int] = ...
    modified_date : Optional[datetime] = ...

    class Config:
        orm_mode=True

class Get_DSS_input_Class(BaseModel):
    cultral_activity_name: str
    cultral_tourism_impact_name: str
    cultral_tourism_objective_name: str
    cultral_tourism_domain_name: str

    class Config:
        orm_mode=True

db=SessionLocal()

#landing endpoint
@app.get('/',tags=["Welcome"]) 
def welcome():
    return {"Impactour says hello"}

#######################
#domain_table endpoints
#######################
@app.get('/domain_table',response_model=List[Domain_Class],tags=["Domain_Table"],status_code=status.HTTP_200_OK)
def get_all_rows():
    items=db.query(impactour_models.Domain_Class).all()

    # json_compatible_item_data = jsonable_encoder(items)
    # return JSONResponse(content=json_compatible_item_data)

    return items

@app.get('/domain_table/{domain_id}',response_model=List[Domain_Class],tags=["Domain_Table"],status_code=status.HTTP_200_OK)
def get_a_row_by_domain_id(domain_id:int):
    items=db.query(impactour_models.Domain_Class).filter(impactour_models.Domain_Class.id==domain_id).all()
    if not items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Domain Not Found")

    return items

@app.get('/domain_table/by_name/{name}',response_model=List[Domain_Class],tags=["Domain_Table"],status_code=status.HTTP_200_OK)
def get_a_row_by_name(name:str):
    item=db.query(impactour_models.Domain_Class).filter(func.lower(impactour_models.Domain_Class.domain_name)==func.lower(name)).all()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Domain Not Found")
    return item


@app.post('/domain_table',response_model=Domain_Class,tags=["Domain_Table"],status_code=status.HTTP_201_CREATED)
def create_a_domain(domain_table_item:Domain_Class):
    db_item=db.query(impactour_models.Domain_Class).filter(func.lower(impactour_models.Domain_Class.domain_name)==func.lower(domain_table_item.domain_name)).first()

    if db_item:
        raise HTTPException(status_code=400,detail="Item already exists")

    all_items=db.query(impactour_models.Domain_Class).all()
    new_item=impactour_models.Domain_Class(
        id =len(all_items)+1,
        domain_code=domain_table_item.domain_code,
        domain_name=domain_table_item.domain_name,
        attribute_1=domain_table_item.attribute_1,
        attribute_2=domain_table_item.attribute_2,
        attribute_3=domain_table_item.attribute_3,
        created_by=domain_table_item.created_by,
        created_date=domain_table_item.created_date,
        modified_by=domain_table_item.modified_by,
        modified_date=domain_table_item.modified_date
    )

    db.add(new_item)
    db.commit()

    return new_item

@app.put('/domain_table/{id}',response_model=Domain_Class,tags=["Domain_Table"],status_code=status.HTTP_200_OK)
def update_a_domain(id:int,domain_table_item:Domain_Class):
    
    item_to_update=db.query(impactour_models.Domain_Class).filter(impactour_models.Domain_Class.id==id).first()

    if not item_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Resource Not Found")
    
    item_to_update=db.query(impactour_models.Domain_Class).filter(impactour_models.Domain_Class.id==id).first()
    item_to_update.domain_code = domain_table_item.domain_code,
    item_to_update.domain_name = domain_table_item.domain_name,
    item_to_update.attribute_1 = domain_table_item.attribute_1,
    item_to_update.attribute_2 = domain_table_item.attribute_2,
    item_to_update.attribute_3 = domain_table_item.attribute_3,
    item_to_update.modified_by = domain_table_item.modified_by,
    item_to_update.modified_date = domain_table_item.modified_date

    db.commit()

    return item_to_update

# @app.delete('/domain_table/{id}',response_model=Domain_Class,tags=["Domain_Table"],status_code=status.HTTP_200_OK)
# def delete_domain(id:int):
#     item_to_delete=db.query(impactour_models.Domain_Class).filter(impactour_models.Domain_Class.id==id).first()

#     if not item_to_delete:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Resource Not Found")
    
#     db.delete(item_to_delete)
#     db.commit()

#     return item_to_delete

############################
#domain_data_table endpoints
############################
@app.get('/domain_data_table',tags=["Domain_Data_Table"],status_code=status.HTTP_200_OK)
def get_all_rows():
    items=db.query(impactour_models.Domain_data_Class).all()

    return items

@app.get('/domain_data_table/indicator_name/{indicator_name}',tags=["Domain_Data_Table"],status_code=status.HTTP_200_OK)
def get_rows_by_indicator_name(indicator_name:str):

    db_item=db.query(impactour_models.Indicator_Class).filter(func.lower(impactour_models.Indicator_Class.indicator_name)==func.lower(indicator_name)).first()
    if not db_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Indicator Not Found")
    else:
        items=db.query(impactour_models.Domain_data_Class).filter(impactour_models.Domain_data_Class.indicator_id==db_item.id).all()
    
    return items

@app.get('/domain_data_table/pilot_id/{pilot_id}',tags=["Domain_Data_Table"],status_code=status.HTTP_200_OK)
def get_rows_by_pilot_id(pilot_id:int):
    items=db.query(impactour_models.Domain_data_Class).filter(impactour_models.Domain_data_Class.pilot_id==pilot_id).all()
    if not items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Resource Not Found")
    return items

@app.get('/domain_data_table/domain_id/{domain_id}',tags=["Domain_Data_Table"],status_code=status.HTTP_200_OK)
def get_rows_by_domain_id(domain_id:int):
    items=db.query(impactour_models.Domain_data_Class).filter(impactour_models.Domain_data_Class.domain_id==domain_id).all()
    if not items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Resource Not Found")
    return items

@app.get('/domain_data_table/domain_and_pilot_id/{domain_id}',tags=["Domain_Data_Table"],status_code=status.HTTP_200_OK)
def get_rows_by_domain_and_pilot_id(domain_id:int,pilot_id:int):
    items=db.query(impactour_models.Domain_data_Class).filter(and_(impactour_models.Domain_data_Class.domain_id==domain_id,impactour_models.Domain_data_Class.pilot_id==pilot_id)).all()
    if not items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Resource Not Found")
    return items

@app.get('/domain_data_table/data_access_type_id/{data_access_type_id}',tags=["Domain_Data_Table"],status_code=status.HTTP_200_OK)
def get_rows_by_data_access_type_id(data_access_type_id:int):
    items=db.query(impactour_models.Domain_data_Class).filter(impactour_models.Domain_data_Class.data_access_type_id==data_access_type_id).all()
    if not items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Resource Not Found")
    return items

# @app.delete('/domain_data_table/{id}',tags=["Domain_Data_Table"],status_code=status.HTTP_200_OK)
# def delete_one_domain_data_row(id:int):
#     item_to_delete=db.query(impactour_models.Domain_data_Class).filter(impactour_models.Domain_data_Class.id==id).first()

#     if not item_to_delete:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Resource Not Found")
    
#     db.delete(item_to_delete)
#     db.commit()

#     return item_to_delete

@app.post('/domain_data_table_upload_file',tags=["Domain_Data_Table"],status_code=status.HTTP_201_CREATED)
def create_a_domain_data_using_file(domain_name:str,pilot_name:str,created_by:int,upload_file: UploadFile = File(...)):
    
    entry = 0
    bad_indicator_name = "Total Population / Total Area based on Type of Site (Urban or Rural/Natural/Itinerary)"
    domain_name = domain_name.lower()
    tmp = tempfile.NamedTemporaryFile(delete=False)
    try:
        tmp.write(upload_file.file.read())
    except Exception as e:
        raise e

    # file_location = f".{upload_file.filename}"
    # with open(file_location, "wb+") as file_object:
    #     file_object.write(upload_file.file.read())

    try:
        xls = ExcelFile(tmp)
        df = xls.parse(xls.sheet_names[0])
        df = df.drop(df.columns[[0,1]],axis = 1)
        # print(df)
        #df = df.fillna(method='ffill')
        #df = df.fillna('')
        df_value_1 = df[df['VALUE 1'].notna()]
        df_value_2 = df[df['VALUE 2'].notna()]
        df_value_1 = df_value_1.fillna('')
        df_value_2 = df_value_2.fillna('')
    except Exception as e:
        raise e

    for index, row in df_value_1.iterrows():

        new_empty_object = impactour_models.Domain_data_Class()

        db_item=db.query(impactour_models.Domain_Class).filter(func.lower(impactour_models.Domain_Class.domain_name)==domain_name).first()
        if not db_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Domain Not Found")
        else:
            new_empty_object.domain_id = db_item.id

        db_item=db.query(impactour_models.Pilot_Class).filter(func.lower(impactour_models.Pilot_Class.pilot_name)==(pilot_name).lower()).first()
        if not db_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Pilot Not Found")
        else:
            new_empty_object.pilot_id = db_item.id

        INDICATOR_val =  row["INDICATOR"]
        if INDICATOR_val == 'Pilot Name':
            continue
        if INDICATOR_val == bad_indicator_name:
            if row["VALUE 1"] == "Urban":
                VALUE_1_val = 1
            else:
                VALUE_1_val = 2
        else:
            VALUE_1_val = row["VALUE 1"]

        INDICATOR_CODE_val = row["CODE"]

        REFERENCE_DATE_1_val = row["REFERENCE DATE 1"]
        DATA_SOURCE_1 = row["DATA SOURCE 1"]
        DATA_PRIVACY_val = row["DATA PRIVACY"]
        REMARKS_val = row["REMARKS"]

        db_item_name=db.query(impactour_models.Indicator_Class).filter(func.lower(impactour_models.Indicator_Class.indicator_name)==(INDICATOR_val).lower()).first()
        if not db_item_name:
            db_item_code=db.query(impactour_models.Indicator_Class).filter(and_(func.lower(impactour_models.Indicator_Class.indicator_code)==(INDICATOR_CODE_val).lower()),
                    (impactour_models.Indicator_Class.indicator_type)==str(int(VALUE_1_val))).first()
            if not db_item_code:
                
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=" asdfg sdf Indicator Not Found")
            else:
                new_empty_object.indicator_id = db_item_code.id
        else:
            new_empty_object.indicator_id = db_item_name.id
        
        if DATA_PRIVACY_val.lower() == 'public':
            new_empty_object.data_access_type_id = 1
        elif DATA_PRIVACY_val.lower() == 'private':
            new_empty_object.data_access_type_id = 2
        else:
            new_empty_object.data_access_type_id = 3

        db_item=db.query(impactour_models.Domain_data_Class).filter(and_(
        impactour_models.Domain_data_Class.reference_time==REFERENCE_DATE_1_val,
        impactour_models.Domain_data_Class.result==VALUE_1_val,
        impactour_models.Domain_data_Class.pilot_id==new_empty_object.pilot_id,
        impactour_models.Domain_data_Class.indicator_id==new_empty_object.indicator_id,
        impactour_models.Domain_data_Class.domain_id==new_empty_object.domain_id
        )).first()

        if db_item:
            continue
            raise HTTPException(status_code=400,detail="Item already exists with same result and reference time")

        
        db_item=db.query(impactour_models.Domain_data_Class).filter(and_(
        REFERENCE_DATE_1_val=="",
        impactour_models.Domain_data_Class.result==VALUE_1_val,
        impactour_models.Domain_data_Class.pilot_id==new_empty_object.pilot_id,
        impactour_models.Domain_data_Class.indicator_id==new_empty_object.indicator_id,
        impactour_models.Domain_data_Class.domain_id==new_empty_object.domain_id
        )).first()

        if db_item:
            continue
            raise HTTPException(status_code=400,detail="Item already exists with same result, please provide reference time")

        max_id=db.query(impactour_models.Domain_data_Class.id).order_by(impactour_models.Domain_data_Class.id.desc()).first()
        
        if not max_id:
            new_empty_object.id = 1
        else:
            new_empty_object.id = max_id.id+1
        
        new_empty_object.data_type_id = 1
        new_empty_object.result = VALUE_1_val
        new_empty_object.reference_time = REFERENCE_DATE_1_val
        new_empty_object.sources = DATA_SOURCE_1
        new_empty_object.remarks = REMARKS_val
        new_empty_object.attribute_1 = ""
        new_empty_object.attribute_2 = ""
        new_empty_object.attribute_3 = ""
        new_empty_object.created_by = created_by
        new_empty_object.created_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_empty_object.modified_by = 0
        #new_empty_object.modified_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        db.add(new_empty_object)
        db.commit()
        entry += 1

    for index, row in df_value_2.iterrows():

        new_empty_object = impactour_models.Domain_data_Class()

        db_item=db.query(impactour_models.Domain_Class).filter(func.lower(impactour_models.Domain_Class.domain_name)==domain_name).first()
        if not db_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Domain Not Found")
        else:
            new_empty_object.domain_id = db_item.id

        db_item=db.query(impactour_models.Pilot_Class).filter(func.lower(impactour_models.Pilot_Class.pilot_name)==(pilot_name).lower()).first()
        if not db_item:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Pilot Not Found")
        else:
            new_empty_object.pilot_id = db_item.id

        INDICATOR_val =  row["INDICATOR"]
        if INDICATOR_val == 'Pilot Name':
            continue
        if INDICATOR_val == bad_indicator_name:
            if row["VALUE 1"] == "Urban":
                VALUE_2_val = 1
            else:
                VALUE_2_val = 2
        else:
            VALUE_2_val = row["VALUE 2"]

        INDICATOR_CODE_val = row["CODE"]
        
        REFERENCE_DATE_2_val = row["REFERENCE DATE 2"]
        DATA_SOURCE_2 = row["DATA SOURCE 2"]
        DATA_PRIVACY_val = row["DATA PRIVACY"]
        REMARKS_val = row["REMARKS"]

        db_item_name=db.query(impactour_models.Indicator_Class).filter(func.lower(impactour_models.Indicator_Class.indicator_name)==(INDICATOR_val).lower()).first()

        if not db_item_name:
            db_item_code=db.query(impactour_models.Indicator_Class).filter(and_(func.lower(impactour_models.Indicator_Class.indicator_code)==(INDICATOR_CODE_val).lower()),
                    (impactour_models.Indicator_Class.indicator_type)==str(int(VALUE_2_val))).first()
            if not db_item_code:
                # if INDICATOR_val == 'Type of Site (Urban or Rural/Natural)':
                #     temp_name=db.query(impactour_models.Indicator_Class).filter(func.lower(impactour_models.Indicator_Class.indicator_name)==("Total Population / Total Area based on Type of Site (Urban or Rural/Natural/Itinerary)").lower()).first()
                #     new_empty_object.indicator_id = temp_name.id
                # else:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=" 2 Indicator Not Found")
            else:
                new_empty_object.indicator_id = db_item_code.id
        else:
            new_empty_object.indicator_id = db_item_name.id
        
        if DATA_PRIVACY_val.lower() == 'public':
            new_empty_object.data_access_type_id = 1
        elif DATA_PRIVACY_val.lower() == 'private':
            new_empty_object.data_access_type_id = 2
        else:
            new_empty_object.data_access_type_id = 3

        db_item=db.query(impactour_models.Domain_data_Class).filter(and_(
        impactour_models.Domain_data_Class.reference_time==REFERENCE_DATE_2_val,
        impactour_models.Domain_data_Class.result==VALUE_2_val,
        impactour_models.Domain_data_Class.pilot_id==new_empty_object.pilot_id,
        impactour_models.Domain_data_Class.indicator_id==new_empty_object.indicator_id,
        impactour_models.Domain_data_Class.domain_id==new_empty_object.domain_id
        )).first()

        if db_item:
            continue
            raise HTTPException(status_code=400,detail="Item already exists with same result and reference time")

        db_item=db.query(impactour_models.Domain_data_Class).filter(and_(
        REFERENCE_DATE_2_val=="",
        impactour_models.Domain_data_Class.result==VALUE_2_val,
        impactour_models.Domain_data_Class.pilot_id==new_empty_object.pilot_id,
        impactour_models.Domain_data_Class.indicator_id==new_empty_object.indicator_id,
        impactour_models.Domain_data_Class.domain_id==new_empty_object.domain_id
        )).first()

        if db_item:
            continue
            raise HTTPException(status_code=400,detail="Item already exists with same result, please provide reference time")

        max_id=db.query(impactour_models.Domain_data_Class.id).order_by(impactour_models.Domain_data_Class.id.desc()).first()

        if not max_id:
            new_empty_object.id = 1
        else:
            new_empty_object.id = max_id.id+1
        
        new_empty_object.data_type_id = 1
        new_empty_object.result = VALUE_2_val
        new_empty_object.reference_time = REFERENCE_DATE_2_val
        new_empty_object.sources = DATA_SOURCE_2
        new_empty_object.remarks = REMARKS_val
        new_empty_object.attribute_1 = ""
        new_empty_object.attribute_2 = ""
        new_empty_object.attribute_3 = ""
        new_empty_object.created_by = created_by
        new_empty_object.created_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        new_empty_object.modified_by = 0
        #new_empty_object.modified_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        db.add(new_empty_object)
        db.commit()
        entry += 1

    tmp.close()
    os.unlink(tmp.name)
    return {"Number of Record added" : entry}

@app.post('/domain_data_table',response_model=Domain_data_Class,tags=["Domain_Data_Table"],status_code=status.HTTP_201_CREATED)
def create_a_domain_data(domain_data_table_item:Excel_domain_data_Class):

    new_empty_object = impactour_models.Domain_data_Class()
    
    db_item=db.query(impactour_models.Domain_Class).filter(func.lower(impactour_models.Domain_Class.domain_name)==func.lower(domain_data_table_item.domain_name)).first()
    if not db_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Domain Not Found")
    else:
        new_empty_object.domain_id = db_item.id

    db_item=db.query(impactour_models.Pilot_Class).filter(func.lower(impactour_models.Pilot_Class.pilot_name)==func.lower(domain_data_table_item.pilot_name)).first()
    if not db_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Pilot Not Found")
    else:
        new_empty_object.pilot_id = db_item.id

    db_item=db.query(impactour_models.Indicator_Class).filter(func.lower(impactour_models.Indicator_Class.indicator_name)==func.lower(domain_data_table_item.indicator_name)).first()
    if not db_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Indicator Not Found")
    else:
        new_empty_object.indicator_id = db_item.id

    db_item=db.query(impactour_models.Data_access_type_Class).filter(func.lower(impactour_models.Data_access_type_Class.data_access_type_name)==func.lower(domain_data_table_item.data_privacy_name)).first()
    if not db_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Data Access Type Not Found")
    else:
        new_empty_object.data_access_type_id = db_item.id

    db_item=db.query(impactour_models.Domain_data_Class).filter(and_(
        impactour_models.Domain_data_Class.reference_time==domain_data_table_item.reference_time,
        impactour_models.Domain_data_Class.result==domain_data_table_item.result,
        impactour_models.Domain_data_Class.pilot_id==new_empty_object.pilot_id,
        impactour_models.Domain_data_Class.indicator_id==new_empty_object.indicator_id,
        impactour_models.Domain_data_Class.domain_id==new_empty_object.domain_id
    )).first()

    if db_item:
        raise HTTPException(status_code=400,detail="Item already exists with same result and reference time")
    
    db_item=db.query(impactour_models.Domain_data_Class).filter(and_(
        domain_data_table_item.reference_time=="",
        impactour_models.Domain_data_Class.result==domain_data_table_item.result,
        impactour_models.Domain_data_Class.pilot_id==new_empty_object.pilot_id,
        impactour_models.Domain_data_Class.indicator_id==new_empty_object.indicator_id,
        impactour_models.Domain_data_Class.domain_id==new_empty_object.domain_id
    )).first()

    if db_item:
        raise HTTPException(status_code=400,detail="Item already exists with same result, please provide reference time")

    
    max_id=db.query(impactour_models.Domain_data_Class.id).order_by(impactour_models.Domain_data_Class.id.desc()).first()
        
    new_empty_object.id = max_id.id+1
    new_empty_object.data_type_id = 1
    new_empty_object.result = domain_data_table_item.result
    new_empty_object.reference_time = domain_data_table_item.reference_time
    new_empty_object.sources = domain_data_table_item.sources
    new_empty_object.remarks = domain_data_table_item.remarks
    new_empty_object.attribute_1 = domain_data_table_item.attribute_1
    new_empty_object.attribute_2 = domain_data_table_item.attribute_2
    new_empty_object.attribute_3 = domain_data_table_item.attribute_3
    new_empty_object.created_by = domain_data_table_item.created_by
    new_empty_object.created_date = domain_data_table_item.created_date
    new_empty_object.modified_by = domain_data_table_item.modified_by
    new_empty_object.modified_date = domain_data_table_item.modified_date

    db.add(new_empty_object)
    db.commit()

    return new_empty_object

####################
#kpi_table endpoints
####################
@app.get('/kpi_table',response_model=List[KPI_Class],tags=["KPI_Table"],status_code=status.HTTP_200_OK)
def get_all_rows():
    items=db.query(impactour_models.KPI_Class).all()
    
    return items

@app.get('/kpi_table/{kpi_name}',response_model=List[KPI_Class],tags=["KPI_Table"],status_code=status.HTTP_200_OK)
def get_a_row_by_kpi_name(kpi_name:str):
    item=db.query(impactour_models.KPI_Class).filter(func.lower(impactour_models.KPI_Class.kpi_name)==func.lower(kpi_name)).all()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="KPI Not Found")
    return item

@app.get('/kpi_table/domain_name/{domain_name}',response_model=List[KPI_Class],tags=["KPI_Table"],status_code=status.HTTP_200_OK)
def get_rows_by_domain_name(domain_name:str):

    domian_check=db.query(impactour_models.Domain_Class).filter(func.lower(impactour_models.Domain_Class.domain_name)==func.lower(domain_name)).first()
    if not domian_check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Domain Not Found")
    else:
        items=db.query(impactour_models.KPI_Class).filter(impactour_models.KPI_Class.domain_id==domian_check.id).all()
    return items

@app.get('/kpi_table/kpi_code/{kpi_code}',response_model=List[KPI_Class],tags=["KPI_Table"],status_code=status.HTTP_200_OK)
def get_a_row_by_kpi_code(kpi_code:str):
    item=db.query(impactour_models.KPI_Class).filter(func.lower(impactour_models.KPI_Class.kpi_code)==func.lower(kpi_code)).all()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="KPI Not Found")
    return item

@app.post('/kpi_table',response_model=KPI_Class,tags=["KPI_Table"],status_code=status.HTTP_201_CREATED)
def create_a_kpi(kpi_table_item:KPI_Class):
    
    domain_check = db.query(impactour_models.Domain_Class).filter(impactour_models.Domain_Class.id==kpi_table_item.domain_id).first()

    if not domain_check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Domain Not Found")

    db_item=db.query(impactour_models.KPI_Class).filter(func.lower(impactour_models.KPI_Class.kpi_code)==func.lower(kpi_table_item.kpi_code)).first()

    if db_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Item already exists")

    all_items=db.query(impactour_models.KPI_Class).all()
    new_item=impactour_models.KPI_Class(
        id =len(all_items)+1,
        domain_id = kpi_table_item.domain_id,
        kpi_code = kpi_table_item.kpi_code,
        kpi_name = kpi_table_item.kpi_name,
        calculation_method = kpi_table_item.calculation_method,
        unit = kpi_table_item.unit,
        attribute_1 = kpi_table_item.attribute_1,
        attribute_2 = kpi_table_item.attribute_2,
        attribute_3 = kpi_table_item.attribute_3,
        created_by = kpi_table_item.created_by,
        created_date = kpi_table_item.created_date,
        modified_by = kpi_table_item.modified_by,
        modified_date = kpi_table_item.modified_date
    )

    db.add(new_item)
    db.commit()

    return new_item

# @app.delete('/kpi_table/{id}',response_model=KPI_Class,tags=["KPI_Table"],status_code=status.HTTP_200_OK)
# def delete_kpi(id:int):
#     item_to_delete=db.query(impactour_models.KPI_Class).filter(impactour_models.KPI_Class.id==id).first()

#     if not item_to_delete:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Resource Not Found")
    
#     db.delete(item_to_delete)
#     db.commit()

#     return item_to_delete

@app.put('/kpi_table/{id}',response_model=KPI_Class,tags=["KPI_Table"],status_code=status.HTTP_200_OK)
def update_a_kpi(id:int,kpi_table_item:KPI_Class):
    
    item_to_update=db.query(impactour_models.KPI_Class).filter(impactour_models.KPI_Class.id==id).first()

    if not item_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Resource Not Found")
    
    domain_check = db.query(impactour_models.Domain_Class).filter(impactour_models.Domain_Class.id==kpi_table_item.domain_id).first()

    if not domain_check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Domain Not Found")

    item_to_update=db.query(impactour_models.KPI_Class).filter(impactour_models.KPI_Class.id==id).first()
    item_to_update.domain_id = kpi_table_item.domain_id,
    item_to_update.kpi_code = kpi_table_item.kpi_code,
    item_to_update.kpi_name = kpi_table_item.kpi_name,
    item_to_update.calculation_method = kpi_table_item.calculation_method,
    item_to_update.unit = kpi_table_item.unit,
    item_to_update.attribute_1 = kpi_table_item.attribute_1,
    item_to_update.attribute_2 = kpi_table_item.attribute_2,
    item_to_update.attribute_3 = kpi_table_item.attribute_3,
    item_to_update.modified_by = kpi_table_item.modified_by,
    item_to_update.modified_date = kpi_table_item.modified_date

    db.commit()

    return item_to_update

################################
#KPI_calculation_table endpoints
################################
@app.get('/kpi_calculation_table',response_model=List[KPI_calculation_Class],tags=["KPI_calculation_Table"],status_code=status.HTTP_200_OK)
def get_all_rows():
    items=db.query(impactour_models.KPI_calculation_Class).all()

    return items

@app.get('/kpi_calculation_table/pilot_name/{pilot_name}',response_model=List[KPI_calculation_Class],tags=["KPI_calculation_Table"],status_code=status.HTTP_200_OK)
def get_rows_by_pilot_name(pilot_name:str):

    pilot_check=db.query(impactour_models.Pilot_Class).filter(func.lower(impactour_models.Pilot_Class.pilot_name)==func.lower(pilot_name)).first()
    if not pilot_check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Pilot Not Found")
    else:
        items=db.query(impactour_models.KPI_calculation_Class).filter(impactour_models.KPI_calculation_Class.pilot_id==pilot_check.id).all()
    return items

@app.get('/kpi_calculation_table/domain_name/{domain_name}',response_model=List[KPI_calculation_Class],tags=["KPI_calculation_Table"],status_code=status.HTTP_200_OK)
def get_rows_by_domain_name(domain_name:str):

    domian_check=db.query(impactour_models.Domain_Class).filter(func.lower(impactour_models.Domain_Class.domain_name)==func.lower(domain_name)).first()
    if not domian_check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Domain Not Found")
    else:
        items=db.query(impactour_models.KPI_calculation_Class).filter(impactour_models.KPI_calculation_Class.domain_id==domian_check.id).all()
    return items

##########################
#indicator_table endpoints
##########################
@app.get('/indicator_table',response_model=List[Indicator_Class],tags=["Indicator_Table"],status_code=status.HTTP_200_OK)
def get_all_rows():
    items=db.query(impactour_models.Indicator_Class).all()

    return items

@app.get('/indicator_table/{name}',response_model=List[Indicator_Class],tags=["Indicator_Table"],status_code=status.HTTP_200_OK)
def get_a_row_by_name(name:str):
    item=db.query(impactour_models.Indicator_Class).filter(func.lower(impactour_models.Indicator_Class.indicator_name)==func.lower(name)).all()
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Resource Not Found")
    return item

@app.post('/indicator_table',response_model=Indicator_Class,tags=["Indicator_Table"],status_code=status.HTTP_201_CREATED)
def create_an_indicator(indicator_table_item:Indicator_Class):
    
    domain_check = db.query(impactour_models.Domain_Class).filter(impactour_models.Domain_Class.id==indicator_table_item.domain_id).first()

    if not domain_check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Domain Not Found")

    db_item=db.query(impactour_models.Indicator_Class).filter(func.lower(impactour_models.Indicator_Class.indicator_name)==func.lower(indicator_table_item.indicator_name)).first()

    if db_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Item already exists")

    all_items=db.query(impactour_models.Indicator_Class).all()
    new_item=impactour_models.Indicator_Class(
        id =len(all_items)+1,
        domain_id = indicator_table_item.domain_id,
        criteria = indicator_table_item.criteria,
        indicator_code = indicator_table_item.indicator_code,
        indicator_name = indicator_table_item.indicator_name,
        indicator_type = indicator_table_item.indicator_type,
        update_periodicity = indicator_table_item.update_periodicity,
        unit = indicator_table_item.unit,
        attribute_1 = indicator_table_item.attribute_1,
        attribute_2 = indicator_table_item.attribute_2,
        attribute_3 = indicator_table_item.attribute_3,
        created_by = indicator_table_item.created_by,
        created_date = indicator_table_item.created_date,
        modified_by = indicator_table_item.modified_by,
        modified_date = indicator_table_item.modified_date
    )

    db.add(new_item)
    db.commit()

    return new_item

@app.put('/indicator_table/{id}',response_model=Indicator_Class,tags=["Indicator_Table"],status_code=status.HTTP_200_OK)
def update_an_indicator(id:int,indicator_table_item:Indicator_Class):
    
    item_to_update=db.query(impactour_models.Indicator_Class).filter(impactour_models.Indicator_Class.id==id).first()

    if not item_to_update:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Resource Not Found")
    
    domain_check = db.query(impactour_models.Domain_Class).filter(impactour_models.Domain_Class.id==indicator_table_item.domain_id).first()

    if not domain_check:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Domain Not Found")

    item_to_update=db.query(impactour_models.Indicator_Class).filter(impactour_models.Indicator_Class.id==id).first()
    item_to_update.domain_id = indicator_table_item.domain_id,
    item_to_update.criteria = indicator_table_item.criteria,
    item_to_update.indicator_code = indicator_table_item.indicator_code,
    item_to_update.indicator_name = indicator_table_item.indicator_name,
    item_to_update.indicator_type = indicator_table_item.indicator_type,
    item_to_update.update_periodicity = indicator_table_item.update_periodicity,
    item_to_update.unit = indicator_table_item.unit,
    item_to_update.attribute_1 = indicator_table_item.attribute_1,
    item_to_update.attribute_2 = indicator_table_item.attribute_2,
    item_to_update.attribute_3 = indicator_table_item.attribute_3,
    item_to_update.modified_by = indicator_table_item.modified_by,
    item_to_update.modified_date = indicator_table_item.modified_date

    db.commit()

    return item_to_update

# @app.delete('/indicator_table/{id}',response_model=Indicator_Class,tags=["Indicator_Table"],status_code=status.HTTP_200_OK)
# def delete_indicator(id:int):
#     item_to_delete=db.query(impactour_models.Indicator_Class).filter(impactour_models.Indicator_Class.id==id).first()

#     if not item_to_delete:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Resource Not Found")
    
#     db.delete(item_to_delete)
#     db.commit()

#     return item_to_delete

######################
#pilot_table endpoints
######################
@app.get('/pilot_table',response_model=List[Pilot_Class],tags=["Pilot_Table"],status_code=status.HTTP_200_OK)
def get_all_rows():
    items=db.query(impactour_models.Pilot_Class).all()

    return items

@app.get('/pilot_table/{pilot_id}',response_model=List[Pilot_Class],tags=["Pilot_Table"],status_code=status.HTTP_200_OK)
def get_a_row_by_pilot_id(pilot_id:int):
    items=db.query(impactour_models.Pilot_Class).filter(impactour_models.Pilot_Class.id==pilot_id).all()

    return items

@app.post('/pilot_table',response_model=Pilot_Class,tags=["Pilot_Table"],status_code=status.HTTP_201_CREATED)
def create_a_pilot(pilot_table_item:Pilot_Class):
    
    db_item=db.query(impactour_models.Pilot_Class).filter(func.lower(impactour_models.Pilot_Class.pilot_name)==func.lower(pilot_table_item.pilot_name)).first()

    if db_item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Pilot already exists")

    all_items=db.query(impactour_models.Pilot_Class).all()
    new_item=impactour_models.Pilot_Class(
        id =len(all_items)+1,
        pilot_code = pilot_table_item.pilot_code,
        pilot_name = pilot_table_item.pilot_name,
        description = pilot_table_item.description,
        country = pilot_table_item.country,
        attribute_1 = pilot_table_item.attribute_1,
        attribute_2 = pilot_table_item.attribute_2,
        attribute_3 = pilot_table_item.attribute_3,
        created_by = pilot_table_item.created_by,
        created_date = pilot_table_item.created_date,
        modified_by = pilot_table_item.modified_by,
        modified_date = pilot_table_item.modified_date
    )

    db.add(new_item)
    db.commit()

    return new_item

# @app.delete('/pilot_table/{id}',response_model=Pilot_Class,tags=["Pilot_Table"],status_code=status.HTTP_200_OK)
# def delete_pilot(id:int):
#     item_to_delete=db.query(impactour_models.Pilot_Class).filter(impactour_models.Pilot_Class.id==id).first()

#     if not item_to_delete:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Pilot Not Found")
    
#     db.delete(item_to_delete)
#     db.commit()

#     return item_to_delete

##############################
#kpi_indicator_table endpoints
##############################
@app.get('/kpi_indicator_table',response_model=List[KPI_indicator_Class],tags=["KPI_Indicator_Table"],status_code=status.HTTP_200_OK)
def get_all_rows():
    items=db.query(impactour_models.KPI_indicator_Class).all()

    return items

##############################
#DSS endpoints
##############################

# Site Type

@app.get('/dss_filtering/site_types_names',tags=["DSS_Filtering"],status_code=status.HTTP_200_OK)
def get_all_site_types_names():
    items=db.query(impactour_models.Site_Class).order_by(impactour_models.Site_Class.id.asc()).all()
    return items

@app.get('/dss_filtering/site_types_names/{site_id}',tags=["DSS_Filtering"],status_code=status.HTTP_200_OK)
def get_a_site_type_by_site_id(site_id:int):
    items=db.query(impactour_models.Site_Class).filter(impactour_models.Site_Class.id==site_id).all()
    if not items:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Site Type Not Found")
    return items

# Culteral Activity

@app.get('/dss_filtering/culteral_activity_names',tags=["DSS_Filtering"],status_code=status.HTTP_200_OK)
def get_all_culteral_activity_names():
    items=db.query(impactour_models.Cultural_activity_Class).all()
    return items

# Culteral Tourism Impact

@app.get('/dss_filtering/culteral_tourism_impact_names',tags=["DSS_Filtering"],status_code=status.HTTP_200_OK)
def get_all_culteral_tourism_impact_names():
    items=db.query(impactour_models.Cultural_tourism_impact_Class).all()
    return items

# Culteral Tourism Objective

@app.get('/dss_filtering/objective_names',tags=["DSS_Filtering"],status_code=status.HTTP_200_OK)
def get_all_objective_names():
    items=db.query(impactour_models.Cultural_tourism_objective_Class).all()
    return items

# Domain names

@app.get('/dss_filtering/important_domain_names',tags=["DSS_Filtering"],status_code=status.HTTP_200_OK)
def get_all_important_domain_names():
    filter_ids = [3, 4, 5, 6]
    items=db.query(impactour_models.Domain_Class).filter(impactour_models.Domain_Class.id.in_(filter_ids)).all()
    return items

# Culteral Tourism Action

@app.get('/dss_outcome/action_names',tags=["DSS_Outcome"],status_code=status.HTTP_200_OK)
def get_all_action_names():
    items=db.query(impactour_models.Action_Class).all()
    return items

# Culteral Tourism Strategy

@app.get('/dss_outcome/strategy_names',tags=["DSS_Outcome"],status_code=status.HTTP_200_OK)
def get_all_strategy_names():
    items=db.query(impactour_models.Strategy_Class).all()
    return items

@app.post('/dss_outcome/strategy_list_by_DSS',tags=["DSS_Outcome"],status_code=status.HTTP_200_OK)
def get_all_strategy_names(site_type_name:str,dss_row_1:Get_DSS_input_Class,dss_row_2:Get_DSS_input_Class,dss_row_3:Get_DSS_input_Class):
    
    row_1_SN = (site_type_name).lower()
    row_1_CAN = (dss_row_1.cultral_activity_name).lower()
    row_1_CTIN = (dss_row_1.cultral_tourism_impact_name).lower()
    row_1_CTON = (dss_row_1.cultral_tourism_objective_name).lower()
    row_1_CTDN = (dss_row_1.cultral_tourism_domain_name).lower()
    
    row_1_strategy_objective_val = []
    row_1_strategy_impact_val = []
    row_1_strategy_activity_val = []
    row_1_strategy_site_val = []
    row_1_strategy_domain_val = []
    
    if row_1_CAN != "":

        # Site
        SN_id = db.query(impactour_models.Site_Class).filter(func.lower(impactour_models.Site_Class.site_name)==row_1_SN).first()
        if not SN_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Site Not Found") 
        site_strategy_items = db.query(impactour_models.Strategy_site_Class).filter(impactour_models.Strategy_site_Class.site_id == SN_id.id).order_by(impactour_models.Strategy_site_Class.strategy_id.asc()).all()
        for site_strategy_val in site_strategy_items:
            row_1_strategy_site_val.append(site_strategy_val.value)

        # Cultral Activity
        CAN_id = db.query(impactour_models.Cultural_activity_Class).filter(func.lower(impactour_models.Cultural_activity_Class.activity_type)==row_1_CAN).first()
        if not CAN_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Activity Not Found") 
        activity_strategy_items = db.query(impactour_models.Strategy_cultural_activity_Class).filter(impactour_models.Strategy_cultural_activity_Class.cultural_activity_id == CAN_id.id).order_by(impactour_models.Strategy_cultural_activity_Class.strategy_id.asc()).all()
        for activity_strategy_val in activity_strategy_items:
            row_1_strategy_activity_val.append(activity_strategy_val.value)

        # Cultral Impact
        CTIN_id = db.query(impactour_models.Cultural_tourism_impact_Class).filter(func.lower(impactour_models.Cultural_tourism_impact_Class.impact_option)==row_1_CTIN).first()
        if not CTIN_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Impact Not Found") 
        impact_strategy_items = db.query(impactour_models.Strategy_cultural_tourism_impact_Class).filter(impactour_models.Strategy_cultural_tourism_impact_Class.cultural_tourism_impact_id == CTIN_id.id).order_by(impactour_models.Strategy_cultural_tourism_impact_Class.strategy_id.asc()).all()
        for impact_strategy_val in impact_strategy_items:
            row_1_strategy_impact_val.append(impact_strategy_val.value)

        # Cultral Objective
        CTON_id = db.query(impactour_models.Cultural_tourism_objective_Class).filter(func.lower(impactour_models.Cultural_tourism_objective_Class.objective_name)==row_1_CTON).first()
        if not CTON_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Objective Not Found") 
        objective_strategy_items = db.query(impactour_models.Strategy_cultural_tourism_objective_Class).filter(impactour_models.Strategy_cultural_tourism_objective_Class.cultural_tourism_objective_id == CTON_id.id).order_by(impactour_models.Strategy_cultural_tourism_objective_Class.strategy_id.asc()).all()
        for objective_strategy_val in objective_strategy_items:
            row_1_strategy_objective_val.append(objective_strategy_val.value)

        # Cultral Domain
        CTDN_id = db.query(impactour_models.Domain_Class).filter(func.lower(impactour_models.Domain_Class.domain_name)==row_1_CTDN).first()
        if not CTON_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Objective Not Found") 
        domain_strategy_items = db.query(impactour_models.Strategy_domain_Class).filter(impactour_models.Strategy_domain_Class.domain_id == CTDN_id.id).order_by(impactour_models.Strategy_domain_Class.strategy_id.asc()).all()
        for domain_strategy_val in domain_strategy_items:
            row_1_strategy_domain_val.append(domain_strategy_val.value)

    row_2_SN = (site_type_name).lower()
    row_2_CAN = (dss_row_2.cultral_activity_name).lower()
    row_2_CTIN = (dss_row_2.cultral_tourism_impact_name).lower()
    row_2_CTON = (dss_row_2.cultral_tourism_objective_name).lower()
    row_2_CTDN = (dss_row_2.cultral_tourism_domain_name).lower()
    
    row_2_strategy_objective_val = []
    row_2_strategy_impact_val = []
    row_2_strategy_activity_val = []
    row_2_strategy_site_val = []
    row_2_strategy_domain_val = []
    
    if row_2_CAN != "":

        # Site
        SN_id = db.query(impactour_models.Site_Class).filter(func.lower(impactour_models.Site_Class.site_name)==row_2_SN).first()
        if not SN_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Site Not Found") 
        site_strategy_items = db.query(impactour_models.Strategy_site_Class).filter(impactour_models.Strategy_site_Class.site_id == SN_id.id).order_by(impactour_models.Strategy_site_Class.strategy_id.asc()).all()
        for site_strategy_val in site_strategy_items:
            row_2_strategy_site_val.append(site_strategy_val.value)

        # Cultral Activity
        CAN_id = db.query(impactour_models.Cultural_activity_Class).filter(func.lower(impactour_models.Cultural_activity_Class.activity_type)==row_2_CAN).first()
        if not CAN_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Activity Not Found") 
        activity_strategy_items = db.query(impactour_models.Strategy_cultural_activity_Class).filter(impactour_models.Strategy_cultural_activity_Class.cultural_activity_id == CAN_id.id).order_by(impactour_models.Strategy_cultural_activity_Class.strategy_id.asc()).all()
        for activity_strategy_val in activity_strategy_items:
            row_2_strategy_activity_val.append(activity_strategy_val.value)

        # Cultral Impact
        CTIN_id = db.query(impactour_models.Cultural_tourism_impact_Class).filter(func.lower(impactour_models.Cultural_tourism_impact_Class.impact_option)==row_2_CTIN).first()
        if not CTIN_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Impact Not Found") 
        impact_strategy_items = db.query(impactour_models.Strategy_cultural_tourism_impact_Class).filter(impactour_models.Strategy_cultural_tourism_impact_Class.cultural_tourism_impact_id == CTIN_id.id).order_by(impactour_models.Strategy_cultural_tourism_impact_Class.strategy_id.asc()).all()
        for impact_strategy_val in impact_strategy_items:
            row_2_strategy_impact_val.append(impact_strategy_val.value)

        # Cultral Objective
        CTON_id = db.query(impactour_models.Cultural_tourism_objective_Class).filter(func.lower(impactour_models.Cultural_tourism_objective_Class.objective_name)==row_2_CTON).first()
        if not CTON_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Objective Not Found") 
        objective_strategy_items = db.query(impactour_models.Strategy_cultural_tourism_objective_Class).filter(impactour_models.Strategy_cultural_tourism_objective_Class.cultural_tourism_objective_id == CTON_id.id).order_by(impactour_models.Strategy_cultural_tourism_objective_Class.strategy_id.asc()).all()
        for objective_strategy_val in objective_strategy_items:
            row_2_strategy_objective_val.append(objective_strategy_val.value)

        # Cultral Domain
        CTDN_id = db.query(impactour_models.Domain_Class).filter(func.lower(impactour_models.Domain_Class.domain_name)==row_2_CTDN).first()
        if not CTON_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Objective Not Found") 
        domain_strategy_items = db.query(impactour_models.Strategy_domain_Class).filter(impactour_models.Strategy_domain_Class.domain_id == CTDN_id.id).order_by(impactour_models.Strategy_domain_Class.strategy_id.asc()).all()
        for domain_strategy_val in domain_strategy_items:
            row_2_strategy_domain_val.append(domain_strategy_val.value)

    row_3_SN = (site_type_name).lower()
    row_3_CAN = (dss_row_3.cultral_activity_name).lower()
    row_3_CTIN = (dss_row_3.cultral_tourism_impact_name).lower()
    row_3_CTON = (dss_row_3.cultral_tourism_objective_name).lower()
    row_3_CTDN = (dss_row_3.cultral_tourism_domain_name).lower()
    
    row_3_strategy_objective_val = []
    row_3_strategy_impact_val = []
    row_3_strategy_activity_val = []
    row_3_strategy_site_val = []
    row_3_strategy_domain_val = []
    
    if row_3_CAN != "":

        # Site
        SN_id = db.query(impactour_models.Site_Class).filter(func.lower(impactour_models.Site_Class.site_name)==row_3_SN).first()
        if not SN_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Site Not Found") 
        site_strategy_items = db.query(impactour_models.Strategy_site_Class).filter(impactour_models.Strategy_site_Class.site_id == SN_id.id).order_by(impactour_models.Strategy_site_Class.strategy_id.asc()).all()
        for site_strategy_val in site_strategy_items:
            row_3_strategy_site_val.append(site_strategy_val.value)

        # Cultral Activity
        CAN_id = db.query(impactour_models.Cultural_activity_Class).filter(func.lower(impactour_models.Cultural_activity_Class.activity_type)==row_3_CAN).first()
        if not CAN_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Activity Not Found") 
        activity_strategy_items = db.query(impactour_models.Strategy_cultural_activity_Class).filter(impactour_models.Strategy_cultural_activity_Class.cultural_activity_id == CAN_id.id).order_by(impactour_models.Strategy_cultural_activity_Class.strategy_id.asc()).all()
        for activity_strategy_val in activity_strategy_items:
            row_3_strategy_activity_val.append(activity_strategy_val.value)

        # Cultral Impact
        CTIN_id = db.query(impactour_models.Cultural_tourism_impact_Class).filter(func.lower(impactour_models.Cultural_tourism_impact_Class.impact_option)==row_3_CTIN).first()
        if not CTIN_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Impact Not Found") 
        impact_strategy_items = db.query(impactour_models.Strategy_cultural_tourism_impact_Class).filter(impactour_models.Strategy_cultural_tourism_impact_Class.cultural_tourism_impact_id == CTIN_id.id).order_by(impactour_models.Strategy_cultural_tourism_impact_Class.strategy_id.asc()).all()
        for impact_strategy_val in impact_strategy_items:
            row_3_strategy_impact_val.append(impact_strategy_val.value)

        # Cultral Objective
        CTON_id = db.query(impactour_models.Cultural_tourism_objective_Class).filter(func.lower(impactour_models.Cultural_tourism_objective_Class.objective_name)==row_3_CTON).first()
        if not CTON_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Objective Not Found") 
        objective_strategy_items = db.query(impactour_models.Strategy_cultural_tourism_objective_Class).filter(impactour_models.Strategy_cultural_tourism_objective_Class.cultural_tourism_objective_id == CTON_id.id).order_by(impactour_models.Strategy_cultural_tourism_objective_Class.strategy_id.asc()).all()
        for objective_strategy_val in objective_strategy_items:
            row_3_strategy_objective_val.append(objective_strategy_val.value)

        # Cultral Domain
        CTDN_id = db.query(impactour_models.Domain_Class).filter(func.lower(impactour_models.Domain_Class.domain_name)==row_3_CTDN).first()
        if not CTON_id:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Objective Not Found") 
        domain_strategy_items = db.query(impactour_models.Strategy_domain_Class).filter(impactour_models.Strategy_domain_Class.domain_id == CTDN_id.id).order_by(impactour_models.Strategy_domain_Class.strategy_id.asc()).all()
        for domain_strategy_val in domain_strategy_items:
            row_3_strategy_domain_val.append(domain_strategy_val.value)

    if (row_1_CAN != "") and (row_2_CAN != "") and (row_3_CAN != ""):
        impact_min = []
        activity_avg = []
        domain_avg = []

        for row_1,row_2,row_3 in zip(row_1_strategy_impact_val,row_2_strategy_impact_val,row_3_strategy_impact_val):
            impact_min.append(np.min([row_1,row_2,row_3]))

        for row_1,row_2,row_3 in zip(row_1_strategy_activity_val,row_2_strategy_activity_val,row_3_strategy_activity_val):
            activity_avg.append(np.average([row_1,row_2,row_3]))

        for row_1,row_2,row_3 in zip(row_1_strategy_domain_val,row_2_strategy_domain_val,row_3_strategy_domain_val):
            domain_avg.append(np.average([row_1,row_2,row_3]))

        row_1_st_score_a = []
        row_1_st_score_b = []

        for row_1_cto,row_1_site,row_1_impact_min,row_1_act_avg,row_1_domain_avg in zip(row_1_strategy_objective_val, row_1_strategy_site_val, impact_min,activity_avg,domain_avg):
            val_1 = row_1_cto * ((row_1_act_avg + row_1_site) * row_1_impact_min)
            row_1_st_score_a.append(val_1)
            val_2 = val_1 * row_1_domain_avg
            row_1_st_score_b.append(val_2)

        row_2_st_score_a = []
        row_2_st_score_b = []

        for row_2_cto,row_2_site,row_2_impact_min,row_2_act_avg,row_2_domain_avg in zip(row_2_strategy_objective_val, row_2_strategy_site_val, impact_min,activity_avg,domain_avg):
            val_2 = row_2_cto * ((row_2_act_avg + row_2_site) * row_2_impact_min)
            row_2_st_score_a.append(val_2)
            val_2 = val_2 * row_2_domain_avg
            row_2_st_score_b.append(val_2)

        row_3_st_score_a = []
        row_3_st_score_b = []

        for row_3_cto,row_3_site,row_3_impact_min,row_3_act_avg,row_3_domain_avg in zip(row_3_strategy_objective_val, row_3_strategy_site_val, impact_min,activity_avg,domain_avg):
            val_3 = row_3_cto * ((row_3_act_avg + row_3_site) * row_3_impact_min)
            row_3_st_score_a.append(val_3)
            val_3 = val_3 * row_3_domain_avg
            row_3_st_score_b.append(val_3)

        row_final_score = []
        for row_1_b,row_2_b,row_3_b in zip(row_1_st_score_b,row_2_st_score_b,row_3_st_score_b):
            row_final_score.append(np.max([row_1_b,row_2_b,row_3_b]))

        strategy_new_object = db.query(impactour_models.Strategy_Class).order_by(impactour_models.Strategy_Class.id).all()

        for row_final_score_val,att1 in zip(row_final_score,strategy_new_object):
            att1.attribute_1 = row_final_score_val
        
        #final_strategy = strategy_new_object.order_by(float(strategy_new_object.attribute_1).desc()).all()

    if (row_1_CAN != "") and (row_2_CAN != "") and (row_3_CAN == ""):
        impact_min = []
        activity_avg = []
        domain_avg = []

        for row_1,row_2 in zip(row_1_strategy_impact_val,row_2_strategy_impact_val):
            impact_min.append(np.min([row_1,row_2]))

        for row_1,row_2 in zip(row_1_strategy_activity_val,row_2_strategy_activity_val):
            activity_avg.append(np.average([row_1,row_2]))

        for row_1,row_2 in zip(row_1_strategy_domain_val,row_2_strategy_domain_val):
            domain_avg.append(np.average([row_1,row_2]))

        row_1_st_score_a = []
        row_1_st_score_b = []

        for row_1_cto,row_1_site,row_1_impact_min,row_1_act_avg,row_1_domain_avg in zip(row_1_strategy_objective_val, row_1_strategy_site_val, impact_min,activity_avg,domain_avg):
            val_1 = row_1_cto * ((row_1_act_avg + row_1_site) * row_1_impact_min)
            row_1_st_score_a.append(val_1)
            val_2 = val_1 * row_1_domain_avg
            row_1_st_score_b.append(val_2)

        row_2_st_score_a = []
        row_2_st_score_b = []

        for row_2_cto,row_2_site,row_2_impact_min,row_2_act_avg,row_2_domain_avg in zip(row_2_strategy_objective_val, row_2_strategy_site_val, impact_min,activity_avg,domain_avg):
            val_2 = row_2_cto * ((row_2_act_avg + row_2_site) * row_2_impact_min)
            row_2_st_score_a.append(val_2)
            val_2 = val_2 * row_2_domain_avg
            row_2_st_score_b.append(val_2)


        row_final_score = []
        for row_1_b,row_2_b in zip(row_1_st_score_b,row_2_st_score_b):
            row_final_score.append(np.max([row_1_b,row_2_b]))

        strategy_new_object = db.query(impactour_models.Strategy_Class).order_by(impactour_models.Strategy_Class.id).all()

        for row_final_score_val,att1 in zip(row_final_score,strategy_new_object):
            att1.attribute_1 = row_final_score_val
    
    if (row_1_CAN != "") and (row_2_CAN == "") and (row_3_CAN == ""):
        impact_min = []
        activity_avg = []
        domain_avg = []

        for row_1 in row_1_strategy_impact_val:
            impact_min.append(row_1)

        for row_1 in row_1_strategy_activity_val:
            activity_avg.append(row_1)

        for row_1 in row_1_strategy_domain_val:
            domain_avg.append(row_1)

        row_1_st_score_a = []
        row_1_st_score_b = []

        for row_1_cto,row_1_site,row_1_impact_min,row_1_act_avg,row_1_domain_avg in zip(row_1_strategy_objective_val, row_1_strategy_site_val, impact_min,activity_avg,domain_avg):
            val_1 = row_1_cto * ((row_1_act_avg + row_1_site) * row_1_impact_min)
            row_1_st_score_a.append(val_1)
            val_2 = val_1 * row_1_domain_avg
            row_1_st_score_b.append(val_2)

        row_final_score = []
        for row_1_b in row_1_st_score_b:
            row_final_score.append(row_1_b)

        strategy_new_object = db.query(impactour_models.Strategy_Class).order_by(impactour_models.Strategy_Class.id).all()

        for row_final_score_val,att1 in zip(row_final_score,strategy_new_object):
            att1.attribute_1 = row_final_score_val


        #final_strategy = strategy_new_object.order_by(float(strategy_new_object.attribute_1).desc()).all()

    if row_1_CAN != "":
        return strategy_new_object
    else:
        return 

@app.get('/dss_outcome/get_action_list_by_strategy_id',tags=["DSS_Outcome"],status_code=status.HTTP_200_OK)
async def get_action_list_by_strategy_id(strategy_id_1:int, strategy_id_2:int, strategy_id_3:int):
    
    filter_ids = [strategy_id_1, strategy_id_2, strategy_id_3]
    actions_by_strategy_id = db.query(impactour_models.Action_Class).filter(impactour_models.Action_Class.strategy_id.in_(filter_ids)).all()
    indicator_length = []
    for one_action in actions_by_strategy_id:

        kpis_by_action_id = db.query(impactour_models.Action_kpi_Class).filter(and_(
            impactour_models.Action_kpi_Class.action_id == one_action.id,
            impactour_models.Action_kpi_Class.value != 0)).order_by(impactour_models.Action_kpi_Class.value.desc()).all()

        kpi_filter_id = []
        for kpis in kpis_by_action_id:
            kpi_filter_id.append(kpis.kpi_id)
        
        indicator_list = db.query(impactour_models.KPI_indicator_Class).filter(impactour_models.KPI_indicator_Class.kpi_id.in_(kpi_filter_id)).all()
        indicator_length.append(len(indicator_list))

    for att1,num_val in zip(actions_by_strategy_id,indicator_length):
        att1.attribute_1 = num_val
        
    return actions_by_strategy_id

@app.get('/dss_outcome/get_kpi_list_by_action_id',tags=["DSS_Outcome"],status_code=status.HTTP_200_OK)
async def get_kpi_list_by_action_id(pilot_id:int,action_id_1:int, action_id_2:int, action_id_3:int):
    
    filter_ids = [action_id_1, action_id_2, action_id_3]

    kpis_by_action_id=db.query(impactour_models.Action_kpi_Class).filter(and_(
        impactour_models.Action_kpi_Class.action_id.in_(filter_ids),
        impactour_models.Action_kpi_Class.value != 0)).order_by(impactour_models.Action_kpi_Class.value.desc()).all()
    
    kpi_filter_id = []

    for kpis in kpis_by_action_id:
        kpi_filter_id.append(kpis.kpi_id)

    kpi_new_object = db.query(impactour_models.KPI_Class).filter(impactour_models.KPI_Class.id.in_(kpi_filter_id)).all()

    for kpis_by_action,kpi_new_object_name in zip(kpis_by_action_id,kpi_new_object):
        kpis_by_action.attribute_1 = kpi_new_object_name.kpi_name

    kpi_cal_items = db.query(impactour_models.KPI_calculation_Class).filter(impactour_models.KPI_calculation_Class.kpi_id.in_(kpi_filter_id)).all()

    for kpis_by_action,kpi_cal_val in zip(kpis_by_action_id,kpi_cal_items):
        kpis_by_action.attribute_2 = kpi_cal_val.calculated_value

    return kpis_by_action_id
