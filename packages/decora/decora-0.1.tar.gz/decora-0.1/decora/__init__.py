# Python module for control of Colorific bluetooth LED bulbs
#
# Copyright 2016 Matthew Garrett <mjg59@srcf.ucam.org>
#
# This code is released under the terms of the MIT license. See the LICENSE file
# for more details.

import BDAddr
from BluetoothSocket import BluetoothSocket, hci_devba
import socket
import sys
import time

def get_handles(sock):
  start = 1
  handles = {}
  while True:
    response = []
    data = bytearray([0x00])
    startlow = start & 0xff
    starthigh = (start >> 8) & 0xff
    packet = bytearray([0x08, startlow, starthigh, 0xff, 0xff, 0x03, 0x28])
    sock.send(packet)
    data = sock.recv(32)
    for d in data:
      response.append(ord(d))
    if response[0] == 1:
      return handles
    position = 2
    while position < len(data):
      handle = response[position+3] | (response[position+4] << 8)
      handle_id = response[position+5] | (response[position+6] << 8)
      handles[handle_id] = handle
      if handle > start:
        start = handle + 1
      position += 7

def send_packet(sock, handle, data):
  packet = bytearray([0x12, handle, 0x00])
  for item in data:
    packet.append(item)
  sock.send(packet)
  data = sock.recv(32)
  response = []
  for d in data:
    response.append(ord(d))
  return response

def read_packet(sock, handle):
  packet = bytearray([0x0a, handle, 0x00])
  sock.send(packet)
  data = sock.recv(32)
  response = []
  for d in data:
    response.append(ord(d))
  return response

class decora:
  def __init__(self, mac, key=None):
    self.mac = mac
    self.key = key
  def connect(self):
    my_addr = hci_devba(0) # get from HCI0
    dest = BDAddr.BDAddr(self.mac)
    addr_type = BDAddr.TYPE_LE_PUBLIC
    self.sock = BluetoothSocket(socket.AF_BLUETOOTH, socket.SOCK_SEQPACKET, socket.BTPROTO_L2CAP)
    self.sock.bind_l2(0, my_addr, cid=4, addr_type=BDAddr.TYPE_LE_PUBLIC)
    self.sock.connect_l2(0, dest, cid=4, addr_type=addr_type)

    self.handles = {}
    handles = get_handles(self.sock)
    self.handles["state"] = handles[0xff01]
    self.handles["config1"] = handles[0xff02]
    self.handles["config2"] = handles[0xff03]
    self.handles["location1"] = handles[0xff04]
    self.handles["location2"] = handles[0xff05]
    self.handles["event"] = handles[0xff06]
    self.handles["time"] = handles[0xff07]
    self.handles["data"] = handles[0xff08]
    self.handles["name"] = handles[0xff09]

    self.unlock()
    self.update_state()
    data = read_packet(self.sock, self.handles["config1"])
    self.bulbtype = data[1]
    self.maxoutput = data[2]
    self.minoutput = data[3]
    self.defaultoutput = data[4]
    data = read_packet(self.sock, self.handles["config2"])
    self.fadeon = data[1]
    self.fadeoff = data[2]
    self.ledtimeout = data[3]

  def unlock(self):
    if self.key == None:
      self.key = self.get_event(83)[3:]
    self.set_event(83, self.key)
    
  def update_state(self):
    data = read_packet(self.sock, self.handles["state"])
    self.power = data[1]
    self.level = data[2]

  def get_event(self, event):
    packet = bytearray([0x22, event, 0x00, 0x00, 0x00, 0x00])
    send_packet(self.sock, self.handles["event"], packet)
    return read_packet(self.sock, self.handles["event"])

  def set_event(self, event, data):
    packet = bytearray([0x11, event, data[0], data[1], data[2], data[3]])
    send_packet(self.sock, self.handles["event"], packet)

  def set_state(self):
    packet = bytearray([self.power, self.level])
    send_packet(self.sock, self.handles["state"], packet)

  def off(self):
    self.update_state()
    self.power = 0
    self.set_state()

  def on(self):
    self.update_state()
    self.power = 1
    self.set_state()

  def get_on(self):
    self.update_state()
    return self.power

  def set_brightness(self, level):
    self.update_state()
    self.level = level
    self.set_state()

  def get_brightness(self):
    self.update_state()
    return self.level
