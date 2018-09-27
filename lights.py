import websocket
try:
    import thread
except ImportError:
    import _thread as thread
import time

def on_message(ws, message):
    # here update the light strings
    print(message)
    # split message
    (receiver, obj, verb) = message.split(":")
    if (receiver != "Lights")
      return
     ''' Verbs:
          from brides: resetLight, flashLight, offLight
          from app: allLightsOn, allLightsFlash, favoriteGirl, lightOn, allLightsOff
      '''
    if (verb == "resetLight")
      resetLight(obj)
    if (verb == "flashLight")
      flashLight(obj)
    if (verb == "offLight")
      offLight(obj)
    if (verb == "allLightsOn")
      allLightsOn(obj)
    if (verb == "allLightsFlash")
      allLightsFlash(obj)
    if (verb == "allLightsOff")
      allLightsOff(obj)
    if (verb == "favoriteGirl")
      favoriteGirl(obj)
    if (verb == "lightOn")
      lightOn(obj)

def on_error(ws, error):
    print(error)

def on_close(ws):
    print("### closed ###")

def on_open(ws):
    ws.send("client:lights");

if __name__ == "__main__":
    websocket.enableTrace(True)
    ws = websocket.WebSocketApp("ws://ec2-34-201-43-105.compute-1.amazonaws.com:8000",
                              on_message = on_message,
                              on_error = on_error,
                              on_close = on_close)
    ws.on_open = on_open
    ws.run_forever()

def resetLight(obj):
  # obj女嘉宾试图亮灯，一般不处理
  pass

def flashLight(obj):
  # obj女嘉宾试图爆灯，检查状态，确认通道开启而且女嘉宾为亮灯状态后，发送爆灯信息给App，obj开始闪烁

def offLight(obj):
  # obj女嘉宾试图灭灯，检查状态，确认通道开启而且女嘉宾为亮灯状态后，发送obj灭灯信息，熄灭obj

def allLightsOn(obj):
  # 所有灯为点亮状态，通道开启

def allLightsFlash(obj):
  # 庆祝模式，关闭通道，所有灯彩色闪烁状态

def allLightsMusic(obj):
  # 休闲模式，关闭通道，所有灯按照音乐节奏闪烁

def allLightsOff(obj):
  # 关闭通道，所有灯灭

def favoriteGirl(obj):
  # 心动女生为obj，确认通道开启后，obj灯开始闪烁，其他灯状态不变，关闭通道

def lightOn(obj):
  # 无论通道是否开启，都把obj的状态改为点亮，发送亮灯信息，不影响其他灯状态
