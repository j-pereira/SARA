from srs import SRS
from dayevt import DayEvt

url = "ftp://ftp.swpc.noaa.gov/pub/latest/"
url2 = "ftp://ftp.swpc.noaa.gov/pub/warehouse/2018/SRS/"

srs = SRS()
srs.download(url2)
srs.readFile(srs.openFile())
srs.fileLinesLen()

srs.loadRegions()
srs.printRegions()

print("\n ---- \n")


dayevt = DayEvt()
#dayevt.download(url)
dayevt.readFile(dayevt.openFile())
dayevt.fileLinesLen()

dayevt.setHeadersColumnPosition(dayevt.loadFilesHeader())
dayevt.loadEvents()
dayevt.printEvents()


