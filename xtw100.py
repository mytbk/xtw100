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


def xtw100_detect(inep, outep):
    # it's a little bit buggy here, so do it twice
    outep.write('\x00\x09')
    r = inep.read(64)
    outep.write('\x00\x09')
    r = inep.read(64)
    return r


def xtw100_read(inep, outep, size):
    outep.write('\x00\x07')
    inep.read(64)
    outep.write('\x00\x05')
    inep.read(64)
    data = b''
    for i in range(0,size//256):
        data += inep.read(256).tobytes()
    return data

def xtw100_erase():
    pass

def xtw100_write():
    pass


def test_read(inep, outep):
    allbytes = xtw100_read(inep, outep, 8388608)
    xtw100_deinit(outep)
    f = open('/tmp/1.rom', 'wb')
    f.write(allbytes)
    f.close()

dev = usb.core.find(idVendor=0x1fc8, idProduct=0x300b)

# do not use dev.set_configuration()

cfg = dev.get_active_configuration()
intf = cfg[(0,0)]

outep = usb.util.find_descriptor(intf, bEndpointAddress=4)

inep = usb.util.find_descriptor(intf, bEndpointAddress=0x85)

xtw100_deinit(outep)

