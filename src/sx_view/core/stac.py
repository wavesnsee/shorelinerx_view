import pystac
from pathlib import Path
from sx_view.core import raster, waterline, geo_utils, thr_diagram


def read(ls: list, r_ids, f_aoi, plot_td: bool, odir: Path):
    '''
    read list of stac items
    '''

    # create list of pystac objects
    items = [pystac.Item.from_file(f) for f in ls][0:10]

    # read waterlines
    gdf = waterline.read(items)

    # read rasters
    rs = raster.read(items, r_ids, f_aoi, odir)

    # add rasters to gdf
    for r_id in r_ids:
         gdf[r_id] = rs[r_id]

    # read svg threshold diagrams
    if plot_td:
        td = thr_diagram.path(items)
        # add td to gdf
        gdf['f_td'] = td

    # drop lines of the geodataframe corresponding to empty waterline
    gdf = gdf.dropna(subset=["geometry"])

    # clip gdf to aoi
    gdf = geo_utils.clip_gdf(gdf, f_aoi)

    return gdf