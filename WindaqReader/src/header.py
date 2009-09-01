# To change this template, choose Tools | Templates
# and open the template in the editor.
import struct

class header(object):
    header_extent = struct.Struct("<h")
    value_8001H = struct.Struct("<h")
    element27 = struct.Struct("<H")

    def __init__(self,wholefile):
        self.file = wholefile
        self.get_extent()


    def get_extent(self):
        self.file.seek(6)
        self.extent = header.header_extent.unpack(self.file.read(2))[0]
        return self.extent

    def get_value_8001H(self):
        self.file.seek(self.extent-2)
        self.values_8001H = header.value_8001H.unpack(self.file.read(2))
        return self.values_8001H[0]

    def get_is_packed(self):
        self.file.seek(100)
        (whole_27,) = header.element27.unpack(self.file.read(2))
        self.is_packed = whole_27 & 0x0002
        return self.is_packed