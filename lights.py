# -*- coding: utf-8 -*-

import websocket
try:
    import thread
except ImportError:
    import _thread as thread
import time

l = {}
channel = False

def air():
    global channel
    return channel

def setAir(c):
    global channel
    channel = c

def updateLEDs(obj, status):
    pass

def resetLight(obj, ws, l):
  #obj女嘉宾试图亮灯，一般不处理
  print "reset light called"

def flashLight(obj, ws, l):
  # obj女嘉宾试图爆灯，检查状态，确认通道开启而且女嘉宾为亮灯状态后，发送爆灯信息给App，obj开始闪烁
  print "flash light called"
  if (! (obj in l)):
    l[obj] = "null"
  status = l[obj]
  if (status != "on" or ! channelOpen()):
    return
  ws.send("App:" + obj + ":flash")
  updateLEDs(obj, "flash")
  l[obj] = "flash"

def offLight(obj, ws, l):
  # obj女嘉宾试图灭灯，检查状态，确认通道开启而且女嘉宾为亮灯状态后，发送obj灭灯信息，熄灭obj
  print "off light called"
  if (! (obj in l)):
    l[obj] = "null"
  status = l[obj]
  if (status != "on" or ! channelOpen()):
    return
  ws.send("App:" + obj + ":off")
  updateLEDs(obj, "off")
  l[obj] = "off"

def allLightsOn(obj, ws, l):
  # 所有灯为点亮状态，通道开启
  print "all lights on called"
  setAir(True)
  for (i in l):
    l[i] = "on"
    updateLEDs(i, "on")

def allLightsFlash(obj, ws, l):
  # 庆祝模式，关闭通道，所有灯彩色闪烁状态
  print "all lights flash called"
  setAir(False)
  for (i in l):
    l[i] = "flash"
    updateLEDs(i, "flash")

def allLightsMusic(obj, ws, l):
  # 休闲模式，关闭通道，所有灯按照音乐节奏闪烁
  print "all lights music called"
  setAir(False)
  updateLEDs("0", "music")

def allLightsOff(obj, ws, l):
  # 关闭通道，所有灯灭
  print "all lights off called"
  setAir(False)
  for (i in l):
    l[i] = "off"
    updateLEDs(i, "off")

def favoriteGirl(obj, ws, l):
  # 心动女生为obj，确认通道开启后，obj灯开始闪烁，其他灯状态不变，关闭通道
  print "favorite girl called"
  setAir(False)
  l[obj] = "favorite"
  updateLEDs(obj, "favorite")

def lightOn(obj, ws, l):
  # 无论通道是否开启，都把obj的状态改为点亮，发送亮灯信息，不影响其他灯状态
  print "light on called"
  l[obj] = "on"
  updateLEDs(obj, "on")

def on_message(ws, message):
    # here update the light strings
    global l
    print(message)
    # split message
    (receiver, obj, verb) = message.split(":")
    if (receiver != "Lights"):
      return
    ''' Verbs:
          from brides: resetLight, flashLight, offLight
          from app: allLightsOn, allLightsFlash, favoriteGirl, lightOn, allLightsOff
    '''
    if (verb == "resetLight"):
      resetLight(obj, ws, l)
    if (verb == "flashLight"):
      flashLight(obj, ws, l)
    if (verb == "offLight"):
      offLight(obj, ws, l)
    if (verb == "allLightsOn"):
      allLightsOn(obj, ws, l)
    if (verb == "allLightsFlash"):
      allLightsFlash(obj, ws, l)
    if (verb == "allLightsOff"):
      allLightsOff(obj, ws, l)
    if (verb == "favoriteGirl"):
      favoriteGirl(obj, ws, l)
    if (verb == "lightOn"):
      lightOn(obj, ws, l)

    print l

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    print "Connected to hub"

if __name__ == "__main__":
    websocket.enableTrace(True)
    global ws
    ws = websocket.WebSocketApp("ws://ec2-34-201-43-105.compute-1.amazonaws.com:8000",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()