databaseid: 1460
pdfName: Cartopy map gridlines and tick labels  cartopy 0.14.dev0 documentation_xx1460xx.pdf
title: Cartopy map gridlines and tick labels cartopy 0.14.dev0 documentation
subtype: work-projects
author: scitools
url: http://scitools.org.uk/cartopy/docs/latest/matplotlib/gridliner.html 
shareText: 
rating: 
tags: 
action: delete




# Cartopy map gridlines and tick labels 

The Gridliner instance 

has a variety of attributes which can be used to determine draw time behaviour of the gridlines and labels. 

```
cartopy\.mpl.gridliner.Gridliner(axes, crs, draw_labels=False, xlocator=None, ylocator=None, collection_kwargs=None) [source]
```
 

axes 

The cartopy.mpl.geoaxes.GeoAxes object to be drawn on. 

crs 

The cartopy.crs.CRS defining the coordinate system that the gridlines are drawn in. 

draw_labels 

Toggle whether to draw labels. 

xlocator 

Defaults to None, which implies automatic locating of the gridlines. 

ylocator 

Defaults to None, which implies automatic locating of the gridlines. 

collection_kwargs 

Dictionary controlling line properties, passed to matplotlib.collections.Collection. 

```
import matplotlib.pyplot as plt import matplotlib.ticker as mticker import cartopy.crs as ccrs from cartopy.mpl.gridliner import LONGITUDE_FORMATTER, LATITUDE_FORMATTER ax = plt.axes(projection=ccrs.Mercator()) ax.coastlines() gl = ax.gridlines(crs=ccrs.PlateCarree(), draw_labels=True, linewidth=2, color='gray', alpha=0.5, linestyle='  ') gl.xlabels_top = False gl.ylabels_left = False gl.xlines = False gl.xlocator = mticker.FixedLocator([ 180,  45, 0, 45, 180]) gl.xformatter = LONGITUDE_FORMATTER gl.yformatter = LATITUDE_FORMATTER gl.xlabel_style = {'size': 15, 'color': 'gray'} gl.xlabel_style = {'color': 'red', 'weight': 'bold'} plt.show()
```
 

**Clip image from [`Cartopy map gridlines and tick labels  cartopy 0.14.dev0 documentation_xx1460xx.pdf` page 3](dryx-open:///Users/Dave/Dropbox//notes/pdf-notes/Cartopy%20map%20gridlines%20and%20tick%20labels%20%20cartopy%200.14.dev0%20documentation_xx1460xx.pdf)** 

