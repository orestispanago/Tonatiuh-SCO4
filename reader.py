import os
import glob
import sqlite3
import pandas as pd
from pathlib import Path

def get_surface_hits(dbname,surface, side):
    """ Gets count of photon hits on surface from .db file"""
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()
    cursor.execute(f"""SELECT count() FROM Surfaces,Photons
                           WHERE Photons.surfaceID=Surfaces.id 
                           AND Surfaces.Path LIKE '%{surface}%'
                           AND Photons.side = {side};""")
    value = cursor.fetchall()[0][0]
    conn.close()
    return value

def get_wphoton(dbname):
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()
    cursor.execute("SELECT power FROM wphoton;")
    value = cursor.fetchall()[0][0]
    conn.close()
    return value

def get_hits(fname):
    hits =  {
        "sun" : get_surface_hits(fname, "Light", 1),
        "reflectors_back" : get_surface_hits(fname, "Heliostat", 0),
        "reflectors_front" : get_surface_hits(fname, "Heliostat", 1),
        "absorber_bottom" : get_surface_hits(fname, "abs", 0),
        "absorber_top" : get_surface_hits(fname, "abs", 1)
    }
    return hits

def convert_to_w(hits, wphot):
    for key in hits:    
        hits[key] *=  wphot
    return hits

def get_fluxes(fname):
    hits = get_hits(fname)
    wphoton = get_wphoton(fname)
    convert_to_w(hits, wphoton)
    hits.update({"angle" : round(float(os.path.split(fname)[1][:-3]),1)})
    return hits

def read_dir(folder):
    dbfiles = glob.glob(os.getcwd() + f'/{folder}/*.db')
    dbfiles.sort()   
    df = pd.DataFrame(columns=([*get_fluxes(dbfiles[0])]))
    count = 1
    for fname in dbfiles: 
        df.loc[count] = [*get_fluxes(fname).values()]
        count+=1
    df = df.set_index("angle")
    df.sort_index(inplace=True)
    return df

folders = ["ideal-plain/Transversal/raw", "ideal-plain/Longitudinal/raw"]

for folder in folders:
    raw_df = read_dir(folder)
    raw_df.to_csv(f"{Path(folder).parents[0]}/fluxes.csv")
