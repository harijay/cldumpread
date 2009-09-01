import os.path
# To change this template, choose Tools | Templates
# and open the template in the editor.

__author__="hari"
__date__ ="$May 20, 2009 11:13:44 AM$"
from optparse import OptionParser
from header import header
import struct
import csv

class Windaqreader(object):
    winvalue_struct = struct.Struct("<h")
    slope_struct = struct.Struct("<d")
    unit_struct = struct.Struct("<B")
    def __init__(self,file):
        self.file = open(file,"rb")

    def print_header(self):
        h = header(self.file)
        extent = h.get_extent()
        my8001h = h.get_value_8001H()
        print "Header Bytes:%d" % extent
        print "Value  8001H:%d" % my8001h
        print "Is    Packed:%d" % h.get_is_packed()
    def get_slope(self):
        self.file.seek(110)
        self.file.read(4)
        self.file.read(4)

        self.slope = Windaqreader.slope_struct.unpack(self.file.read(8))[0]
        self.intercept = Windaqreader.slope_struct.unpack(self.file.read(8))[0]
        self.tag = self.file.read(6)
        print self.slope , self.intercept, self.tag
        
    def print_data_file(self):
        self.file.seek(1156)
        self.values = []

        try:
            while True:
                data = self.file.read(2)
                if(data == "" ):
                    break
                val1 = Windaqreader.winvalue_struct.unpack(data)[0] >> 2
                true = val1*self.slope + self.intercept
                composite = []
                composite.append(true * -1)
                composite.append(true)
                self.values.append(composite)
           
        except Exception , e:
            #print "Caught Exception while printing list:%d values read : Error %s" % (i,e.message)
            pass

        import os
        self.outfile = open(os.path.splitext(self.file.name)[0] + "_outfile.csv" , "w")
        csvwriter = csv.writer(self.outfile,dialect=csv)
        for val in self.values:
         csvwriter.writerow(val)
        self.outfile.write("\n")
        self.outfile.flush()
        self.outfile.close()




def main():
    parser = OptionParser()
    parser.add_option("-i",dest="file",help="input windaq file",metavar="*.daq")
    (options,spillover) = parser.parse_args()
    wq = Windaqreader(options.file)
    wq.print_header()
    wq.get_slope()
    wq.print_data_file()


if __name__ == "__main__":
    main()
