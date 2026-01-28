import geopandas as gpd
import matplotlib.pyplot as plt
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "GEOGRAPHICAL_DATA"
fp = DATA_DIR / r"Data_Hokkaido\N03-23_01_230101.geojson"

gdf = gpd.read_file(fp)
gdf.plot()
plt.show()