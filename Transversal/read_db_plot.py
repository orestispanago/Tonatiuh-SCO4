import os
import glob
import sqlite3
import pandas as pd
import matplotlib.pyplot as plt



def count_surface_hits(dbname,surface, side):
    """ Gets count of photon hits on surface from .db file"""
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()
    cursor.execute(f"""SELECT count() from Surfaces,Photons
                           where Photons.surfaceID=Surfaces.id 
                           AND Surfaces.Path like '%{surface}%'
                           AND Photons.side = {side};""")
    value = cursor.fetchall()[0][0]
    conn.close()
    return value

def wphoton(dbname):
    """ TODO use to calculate fluxes in next analysis step """
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()
    cursor.execute("SELECT * from wphoton;")
    value = cursor.fetchall()[0][0]
    conn.close()
    return value

def count_all_surfaces(fname):
    surfaces_count = {
        "angle" : int(os.path.split(fname)[1][:-3]),
        "sun" : count_surface_hits(fname, "Light", 1),
        "reflectors_back" : count_surface_hits(fname, "Heliostat", 0),
        "reflectors_front" : count_surface_hits(fname, "Heliostat", 1),
        "absorber_bottom" : count_surface_hits(fname, "abs", 0),
        "absorber_top" : count_surface_hits(fname, "abs", 1)
    }
    return surfaces_count


def read_files():
    dbfiles = glob.glob(os.getcwd() + '/raw/*.db')
    dbfiles.sort()
    df = pd.DataFrame(columns=([*count_all_surfaces(dbfiles[0]),"wphoton"]))
    for count, fname in enumerate(dbfiles): 
        print(fname)
        df.loc[count] = [*count_all_surfaces(fname).values(), wphoton(fname)]
    df = df.set_index("angle")
    return df

raw_df = read_files()

df = pd.DataFrame(index=raw_df.index)

df["sun"] = raw_df["sun"] * raw_df["wphoton"]
df["incident"] = (raw_df["sun"] - raw_df["absorber_top"]) * raw_df["wphoton"]
df["absorbed"] = raw_df["absorber_bottom"] * raw_df["wphoton"]
df["reflected"] = raw_df["reflectors_front"] * raw_df["wphoton"]
df["missing"] = raw_df["reflectors_back"] * raw_df["wphoton"]
df["gaps"] = df["incident"] - df["reflected"]


plt.plot(df["reflected"])
plt.plot(df["absorbed"])
plt.plot(df["incident"])
plt.plot(df["sun"])
plt.show()

df["int_f_duffie"] = df["absorbed"] / df["reflected"]
plt.plot(df["int_f_duffie"])
plt.show()

df["int_f_germ"] = df["absorbed"] / df["incident"]
plt.plot(df["int_f_germ"] )
plt.show()

df["my_total"] = df["incident"] -df["reflected"]- df["gaps"]

plt.plot(df["my_total"])
plt.show()