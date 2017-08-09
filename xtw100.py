#!/usr/bin/env python3
#
# Copyright (C) 2017 Iru Cai <mytbk920423@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301 USA
#

import usb.core
import usb.util

def xtw100_deinit(outep):
    outep.write('\x01\x08')


def xtw100_cmd_begin(inep, outep):
    outep.write(b'\x00\x07')
    return inep.read(64)


def xtw100_detect(inep, outep):
    # it's a little bit buggy here, so do it twice
    outep.write('\x00\x09')
    r = inep.read(64)
    outep.write('\x00\x09')
    r = inep.read(64)
    return r


def xtw100_read(inep, outep, size):
    xtw100_cmd_begin(inep, outep)
    outep.write('\x00\x05')
    inep.read(64)
    data = b''
    for i in range(0,size//256):
        data += inep.read(256).tobytes()
    return data


# xtw100_erase: refer to fcn.00405168
def xtw100_erase(inep, outep):
    print(xtw100_cmd_begin(inep, outep))
    # cmd[0:2] = \x01\x02
    # cmd[0x11:2] is \x00\x80 for MX65L6445E
    outep.write(b'\x01\x02'+b' '*15+b'\x00\x80')
    working = 1
    while working:
        outep.write(b'\x00\x0a')
        working = inep.read(64)[0]


def xtw100_write(inep, outep, data, size):
    print(xtw100_cmd_begin(inep, outep))
    # cmd[0:2] = \x00\x05
    # cmd[8:12] is needed
    outep.write(b'\x00\x05'+b' '*6+b'\x00\x00\x00\x00')
    i = 0
    while i < size:
        outep.write(data[i:i+256])
        i += 256


def test_read(inep, outep):
    allbytes = xtw100_read(inep, outep, 8388608)
    xtw100_deinit(outep)
    f = open('/tmp/1.rom', 'wb')
    f.write(allbytes)
    f.close()


def test_erase(inep, outep):
    xtw100_erase(inep, outep)
    xtw100_deinit(outep)


def test_write(inep, outep):
    testdata = bytearray(8388608)
    for i in range(0, 0x8000):
        for j in range(0, 256):
            testdata[i*256+j] = (i+j)&0xff
    xtw100_write(inep, outep, testdata, 8388608)


dev = usb.core.find(idVendor=0x1fc8, idProduct=0x300b)

# do not use dev.set_configuration()

cfg = dev.get_active_configuration()
intf = cfg[(0,0)]

outep = usb.util.find_descriptor(intf, bEndpointAddress=4)

inep = usb.util.find_descriptor(intf, bEndpointAddress=0x85)

xtw100_deinit(outep)

