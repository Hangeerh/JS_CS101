import pandas as pd
import numpy as np
import seaborn as sns
import plotly.express as px
import altair as alt
import time
import matplotlib as mpl
import matplotlib.pyplot as plt
from utils.download_tool import download_dataset, dataset_path


def main():
    ##################################################
    # Download dataset:
    #       https://catalog.data.gov/dataset/traffic-crashes-crashes
    ##################################################

    download_dataset()

    start = time.time()
    df = pd.read_csv(dataset_path)
    end = time.time()

    print(
        f"Stored dataset locally! It took {end-start:.2f} seconds to load into dataframe."
    )
    print(df.head())
    print(df.shape)

    ##################################################
    # General Data cleaning that helps all of the team
    ##################################################
    # drop duplicate rows
    df = df.drop_duplicates()

    # drop some useless columns
    df = df.drop(columns=["CRASH_RECORD_ID", "CRASH_DATE_EST_I", "DOORING_I"])

    # Clean up CRASH_DATE by converting to datatype
    if df["CRASH_DATE"].dtype != "datetime":
        df["CRASH_DATE"] = pd.to_datetime(df["CRASH_DATE"])
    earliest_date = df["CRASH_DATE"].min()
    latest_date = df["CRASH_DATE"].max()

    # These entries are too long to be used as labels for the x- or y-axis
    df["TRAFFIC_CONTROL_DEVICE_SHORT"] = df["TRAFFIC_CONTROL_DEVICE"].replace(
        {
            "TRAFFIC SIGNAL": "SIGNAL",
            "STOP SIGN/FLASHER": "STOP/FLASHER",
            "NO CONTROLS": "NO CTRL",
            "PEDESTRIAN CROSSING SIGN": "PED XING",
            "OTHER RAILROAD CROSSING": "OTHER RR XING",
            "RAILROAD CROSSING GATE": "RR GATE",
            "RR CROSSING SIGN": "RR XING",
            "OTHER REG. SIGN": "REG SIGN",
            "LANE USE MARKING": "LANE MARKS",
            "FLASHING CONTROL SIGNAL": "FLASHER",
            "BICYCLE CROSSING SIGN": "BIKE XING",
            "OTHER WARNING SIGN": "OTHER WARNING",
        }
    )

    df["DEVICE_CONDITION_SHORT"] = df["DEVICE_CONDITION"].replace(
        {
            "FUNCTIONING PROPERLY": "FUNC PROPER",
            "FUNCTIONING IMPROPERLY": "FUNC IMPR",
            "WORN REFLECTIVE MATERIAL": "WORN REFL",
            "NOT FUNCTIONING": "BROKEN",
        }
    )

    # Drop columns that now have substitutes. Do this so the dataset is smaller.
    df = df.drop(columns=["TRAFFIC_CONTROL_DEVICE", "DEVICE_CONDITION"])

    ##################################################
    # Seaborn Plot #1
    #    To determine whether traffic crashes occur more often when controls are present or absent.
    #    --- Need to clean up data so that if TRAFFIC_CONTROL_DEVICE_SHORT == UNKNOWN, then it does not
    #        effect our data.
    ##################################################

    # Remove all rows with TRAFFIC_CONTROL_DATA_SHORT == UNKNOWN
    df_wo_unkn = df[df["TRAFFIC_CONTROL_DEVICE_SHORT"] != "UNKNOWN"].copy()

    df_wo_unkn["CONTROL_EXISTS"] = "Has Control Device"
    df_wo_unkn.loc[
        df_wo_unkn["TRAFFIC_CONTROL_DEVICE_SHORT"] == "NO CTRL", "CONTROL_EXISTS"
    ] = "No Control Device"


    plt.figure(figsize = (10,6))

    ax = sns.countplot(
        data=df_wo_unkn, x="CONTROL_EXISTS", hue="CONTROL_EXISTS"
    )
    plt.suptitle("SEABORN COUNTPLOT How Many Crashes With and Without Traffic Control")
    plt.title(f"Dates: {earliest_date} - {latest_date}")
    plt.xlabel("Existence of Traffic Control Device")
    plt.ylabel("Count")

    for container in ax.containers:
        labels = [f"{int(v):,}" for v in container.datavalues]
        ax.bar_label(container, labels=labels, padding=3)

    max_count = df_wo_unkn["CONTROL_EXISTS"].value_counts().max()
    ax.set_ylim(0, max_count * 1.15)
    plt.show()

    counts = df_wo_unkn["CONTROL_EXISTS"].value_counts(normalize=True) * 100
    order = ["Has Control Device", "No Control Device"]
    counts = counts.reindex(order)

    colors_wanted = sns.color_palette(
        "magma", len(counts)
    )  # use only as many colors as needed

    plt.figure(figsize = (10,6))
    ax = sns.barplot(
        x=counts.index,
        y=counts.values,
        hue=counts.index,
        palette=colors_wanted,
        legend=False,
    )
    plt.suptitle(
        "SEABORN BARPLOT How Many Crashes With and Without Traffic Control (Percentages)",
        y=0.95,
    )
    plt.title(f"Dates: {earliest_date} - {latest_date}")
    plt.xlabel("Existence of Traffic Control Device")
    plt.ylabel("Percentage")

    # Add percent labels on top
    for i, v in enumerate(counts.values):
        ax.text(i, v + 0.8, f"{v:.1f}% of total", ha="center", fontsize=11)

    ax.set_ylim(0, max(counts.values) + 40)  # Make y-axis go up to 100
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    main()
