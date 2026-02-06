import geopandas as gpd
import matplotlib.pyplot as plt
from pathlib import Path

DATA_DIR = Path(__file__).resolve().parent.parent / "GEOGRAPHICAL_DATA"
fp = DATA_DIR / r"Japan_map\N03-20250101.shp"

gdf = gpd.read_file(fp)
gdf.plot()
plt.show()