import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

sns.set_theme()

params = {'figure.figsize': (9,6),
          'axes.titlesize': 20,
          'axes.titleweight': 'bold',
          'axes.labelsize': 20,
          'axes.labelweight': 'bold',
          'xtick.labelsize': 20,
          'ytick.labelsize': 20,
          'font.weight': 'bold',
          'font.size': 20,
          'legend.fontsize': 16,
          'savefig.format': 'png',
          # 'savefig.dpi': 300.0,
          'figure.constrained_layout.use': True}
plt.rcParams.update(params)


def mkdir_if_not_exists(dirname):
    if not os.path.exists(dirname):
        os.makedirs(dirname)

def get_label(string):
    if string.isupper():
        return string
    return string.title().replace("_", " ")

def contains_flux_or_losses(main_str_list, substr_list=["flux", "losses"]):
    for m in main_str_list:
        for s in substr_list:
            if s in m:
                return True
    return False

def plot_quantities(df, quantities_list):
    """ Plots list of df columns in same plot """
    pic_path = os.path.join(df.direction, df.geometry, 
                            "pics", "-".join(quantities_list))
    mkdir_if_not_exists(os.path.dirname(pic_path))
    fig, ax = plt.subplots(figsize=(9, 6))
    for col in quantities_list:
        ax.plot(df[col], label=get_label(col))
    ax.set_xlabel("$\\theta_z \quad  (\degree)$")
    if contains_flux_or_losses(quantities_list):
        ax.set_ylabel("Watts")
    ax.legend()
    plt.savefig(pic_path)
    plt.show()

def plot_geometries_comparison(df_list, quantity):
    """ Plots a column of each dataframe """
    ylabel = get_label(quantity)
    fig, ax = plt.subplots(figsize=(9, 6))
    for df in df_list:
        ax.plot(df[quantity], label=df.geometry)
    ax.set_xlabel("$\\theta_z \quad  (\degree)$")
    ax.set_ylabel(get_label(quantity))
    if contains_flux_or_losses([quantity]):
        ylabel = ylabel + " (W)"
    ax.set_ylabel(ylabel)
    ax.legend()
    fig.savefig(f"comparison-plots/{df.direction}_{quantity}")
    plt.show()

def calc(fname):
    df = pd.read_csv(fname, index_col="angle")
    df.index = df.index - 180
    df["sun"] = df["sun"]
    df["incident_flux"] = df["sun"] - df["absorber_top"]
    df["absorbed_flux"] = df["absorber_bottom"]
    df["reflected_flux"] = df["reflectors_front"]
    df["missing_losses"] = df["reflectors_back"]
    df["gap_losses"] = df["incident_flux"] - df["reflected_flux"]
    df["total_flux"] = df["incident_flux"] - df["reflected_flux"]- \
                                           - df["gap_losses"]
    df["intercept_factor"] = df["absorbed_flux"] / df["reflected_flux"]
    df["intercept_factor_comsol"] = df["absorbed_flux"] / df["incident_flux"]
    df.direction = fname.split("/")[1]
    df.geometry = fname.split("/")[0]
    return df

# FOLDER = "errors-plain/Longitudinal"
# df = calc(f"{FOLDER}/fluxes.csv")


# plot_quantities(df, ["reflected_flux", "absorbed_flux", "incident_flux", "sun"])
# plot_quantities(df, ["absorbed_flux"])
# plot_quantities(df, ["missing_losses"])
# plot_quantities(df, ["gap_losses"])

# plot_quantities(df, ["intercept_factor"] )
# plot_quantities(df, ["intercept_factor_comsol"])



ideal_long = calc("ideal-plain/Longitudinal/fluxes.csv")
ideal_transv = calc("ideal-plain/Transversal/fluxes.csv")
errors_long = calc("errors-plain/Longitudinal/fluxes.csv")
errors_transv = calc("errors-plain/Transversal/fluxes.csv")

plot_geometries_comparison([ideal_transv,errors_transv],"sun")
