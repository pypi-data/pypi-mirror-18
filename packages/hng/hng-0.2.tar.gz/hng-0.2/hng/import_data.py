from markdown import markdown
import pandas as pd
import numpy as np
from pymongo import MongoClient

def joke():
    """It's a joke, you fool!"""
    return markdown("HAHA!")

def import_lab_data():
    """
    import_lab_data         :function to get *all* pure raw lab data (for all patients/encounters)
    parameters              :None
    returns                 :all labs data from DB
    """
    client = MongoClient("mongodb://localhost:27017")
    db = client.hng_ml  #change DB name in production code
    labs = hng.native_lab_procedures
    labs = pd.DataFrame(list(labs.find({},{'_id':0,'lab_procedure_name':1, 'encounter_id':1, 'numeric_result':1})))
    labs.numeric_result = labs.numeric_result.replace('', np.nan)
    labs.numeric_result = labs.numeric_result.astype(float)
    return labs #end of function

def fill_gaussian(df):
    """
    fill_gaussian           :function to fill missing values using Gaussian distribution
    parameters              :labs DataFrame
    returns                 :labs DataFrame with missing values filled with Gaussian distribution
    """
    

def fill_na(df):
    """
    fillna                  :function to fill missing values with 0.0 on any df
    parameters              :DataFrame
    returns                 :DataFrame with missings filled with 0.0
    """


