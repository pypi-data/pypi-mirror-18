from pygeoc.hydro import *
from pygeoc.raster import *
from pygeoc.utils import *
from pygeoc.vector import *

if __name__ == '__main__':
    print D8DIR_TD_VALUES
    dem = r'e:/test/pvdem.tif'
    demR = ReadRaster(dem)
    print RasterStatistics(dem)
