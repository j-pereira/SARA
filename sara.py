from srs import SRS
from sgas import SGAS

urlSRS = "ftp://ftp.swpc.noaa.gov/pub/warehouse/2018/SRS/"
urlSGAS = "ftp://ftp.swpc.noaa.gov/pub/warehouse/2018/SGAS/"

srs = SRS()
srs.download(urlSRS)
srs.readFile(srs.openFile())
srs.fileLinesLen()

srs.loadRegions()
srs.printRegions()

print("\n ---- \n")

sgas = SGAS()
#sgas.download(urlSGAS)
sgas.readFile(sgas.openFile())
sgas.fileLinesLen()

sgas.setHeadersColumnPosition(sgas.loadFilesHeader())
sgas.loadEvents()
sgas.printEvents()


