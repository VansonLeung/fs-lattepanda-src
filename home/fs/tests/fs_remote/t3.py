import socket
import sys
import select
from time import sleep
import asyncio
import math
 
 
 
 
 
# SERVER
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ("0.0.0.0", 8101)
s.bind(server_address)
s.setblocking(0)
print("Do Ctrl+c to exit the program !!")
 
 
 
 
 
# GPIO
# board = pyfirmata.Arduino('/dev/ttyACM0')
 
# iter8 = pyfirmata.util.Iterator(board)
# iter8.start()
 
# pin_SX = board.get_pin('d:9:s')
# pin_SY = board.get_pin('d:10:s')
# pin_SZ = board.get_pin('d:11:s')
 
 
 
 
def dbgPrint(*values: object):
  print(values)
  pass
 
 
 
 
# SERVO
def move_S(sx, sy, sz, sd, sf):
  move_SX(sx)
  move_SY(sy)
  move_SZ(sz)

  if (sd == -1):
    print(f"\t{sx}\t\t{sy}\t\t{sz} end A",)

  elif (sf == -1):
    print(f"\t{sx}\t\t{sy}\t\t{sz}\t\t{sd}\t end B",)
    
  else:
    speedOffsetResult = 0
    if (sf > -1):
      speedOffsetResult = get_decimal_int_speed_offset(chr(sf))

    print(f"\t{sx}\t\t{sy + speedOffsetResult}\t\t{sz}\t\t{sd}\t\t{sf}\t end C",)

  pass

def move_SX(a):
    if (a <= 0):
      return
    # dbgPrint("move_SX", a)
    driftFactor = SD / 10;
 
    fsx = (
      a 
      + driftFactor * ((current_mpu_gyro[2] if current_mpu_gyro is not None else 0)) 
    )
 
    if (fsx < 40):
      fsx = 40
    if (fsx > 140):
      fsx = 140
 
    # pin_SX.write(
    #   fsx
    # )
 
 
def move_SY(a):
    if (a <= 0):
      return
 
    speed = a
    speedOffset = 0
 
    if (SF != -1):
        speedOffset = get_decimal_int_speed_offset(SF)
 
    finalSpeed = speed + speedOffset
 
    finalSpeed = max(0, finalSpeed)
    finalSpeed = min(126, finalSpeed)
 
    # dbgPrint("move_SY", speed, speedOffset, finalSpeed)
    # pin_SY.write(finalSpeed)
 
 
def move_SZ(a):
    if (a <= 0):
      return
    # dbgPrint("move_SZ", a)
    # pin_SZ.write(a)
 
 
 
# RUNTIME
 
SX = -1;
SX_READY = False;
 
SY = -1;
SY_READY = False;
 
SZ = -1;
SZ_READY = False;
 
SD = -1;
SD_READY = False;
 
SF = -1;
SF_READY = False;
 
SIGNAL_BUSY = False;
 
buffer = "";
 
 
 
current_not_recv_server = True
 
 
 
 
current_mpu_acc = None
current_mpu_gyro = None
current_mpu_mag = None
 
 
 
 
 
# ARD:RESET
 
def ad_resetParams():
  global SX;
  global SY;
  global SZ;
  global SD;
  global SF;
 
  global SX_READY;
  global SY_READY;
  global SZ_READY;
  global SD_READY;
  global SF_READY;
  global SIGNAL_BUSY;
 
  SX = -1;
  SY = -1;
  SZ = -1;
  SD = -1;
  SF = -1;
 
  SX_READY = False;
  SY_READY = False;
  SZ_READY = False;
  SD_READY = False;
  SF_READY = False;
  SIGNAL_BUSY = False;
 
 
def ad_resetSpeed():
  global SX;
  global SY;
  global SZ;
  global SD;
  global SF;
 
  SX = 85;
  SY = 95;
  SZ = 85;
  SD = -1;
  SF = -1;
 
  move_S(SX, SY, SZ, SD, SF)
  print("---- ad_resetSpeed ----")
 
 
 
 
 
step = 0
decimal_map = {
  "A": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
  "B": [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
  "C": [0, 0, 0, 0, 1, 0, 0, 0, 0, 1],
  "D": [0, 0, 1, 0, 0, 1, 0, 0, 1, 0],
  "E": [0, 1, 0, 1, 0, 0, 1, 0, 1, 0],
  "F": [0, 1, 0, 1, 0, 1, 0, 1, 0, 1],
  "G": [0, 1, 0, 1, 1, 0, 1, 0, 1, 1],
  "H": [0, 1, 1, 0, 1, 1, 0, 1, 1, 1],
  "I": [0, 1, 1, 1, 1, 0, 1, 1, 1, 1],
  "J": [0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
  "K": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
}
 
def get_decimal_int_speed_offset(sf):
  global step
 
  speed_offset = 0
 
  if sf in decimal_map:
    speed_offset = decimal_map[sf][step]
 
  step += 1
  if step >= 10:
    step = 0
 
  return speed_offset
 
 
 
 
 
# ARD:MANIPULATE
 
CURSOR_INDEX = -1;
 
CH_SX = '!';
CH_SY = '*';
CH_SZ = '#';
CH_SD = '#';
CH_SF = '#';
CH_END = '\n';
 
def ad_manipulate(ch):
 
  global CURSOR_INDEX;
  global SX;
  global SY;
  global SZ;
  global SD;
  global SF;
  global SX_READY;
  global SY_READY;
  global SZ_READY;
  global SD_READY;
  global SF_READY;
  global SIGNAL_BUSY;
  

  dbgPrint("sss", SIGNAL_BUSY, SX_READY, SY_READY, SZ_READY, SD_READY, SF_READY)
  
  if (not SIGNAL_BUSY and not SX_READY):
    if (ch == '!'):
      dbgPrint("--G")
      SIGNAL_BUSY = True
      SX_READY = True
      return False
 
  elif (SIGNAL_BUSY and SX_READY and SX == -1):
    SX = ord(ch)
    return False
 
  elif (SIGNAL_BUSY and SX_READY and SX != -1 and not SY_READY and ch == '*'):
    dbgPrint("--O")
    SY_READY = True
    return False
 
  elif (SIGNAL_BUSY and SX_READY and SX != -1 and SY_READY and SY == -1):
    dbgPrint("--D")
    SY__ = ord(ch)
    if (SY__ < 0):
      SY__ = 95
    elif (SY__ > 127):
      SY__ = 95
 
    if (SY__ < 57):
      SY__ = 57
    elif (SY__ > 124):
      SY__ = 124
 
    SY = SY__
 
    return False
 
 
  elif (SIGNAL_BUSY and SX_READY and SX != -1 and SY_READY and SY != -1 and not SZ_READY and ch == '#'):
    dbgPrint("--K")
    SZ_READY = True
    dbgPrint(SZ)
    return False
 
  elif (SIGNAL_BUSY and SX_READY and SX != -1 and SY_READY and SY != -1 and SZ_READY and SZ == -1):
    dbgPrint("--S")
    SZ = ord(ch)
    return False
 
  elif (SIGNAL_BUSY and SX_READY and SX != -1 and SY_READY and SY != -1 and SZ_READY and SZ != -1 and not SD_READY and ch == '#'):
    dbgPrint("--D1")
    SD_READY = True
    dbgPrint(SD)
    return False
 
  elif (SIGNAL_BUSY and SX_READY and SX != -1 and SY_READY and SY != -1 and SZ_READY and SZ != -1 and SD_READY and SD == -1):
    dbgPrint("--D2")
    SD = ord(ch)
    return False
 
  elif (SIGNAL_BUSY and SX_READY and SX != -1 and SY_READY and SY != -1 and SZ_READY and SZ != -1 and SD_READY and SD != -1 and not SF_READY and ch == '#'):
    dbgPrint("--F1")
    SF_READY = True
    dbgPrint(SF)
    return False
 
  elif (SIGNAL_BUSY and SX_READY and SX != -1 and SY_READY and SY != -1 and SZ_READY and SZ != -1 and SD_READY and SD != -1 and SF_READY and SF == -1):
    dbgPrint("--F2")
    SF = ord(ch)
    return False
 
  elif (
    (SIGNAL_BUSY and SX_READY and SX != -1 and SY_READY and SY != -1 and SZ_READY and SZ != -1 and ch == '\n')
    or
    (SIGNAL_BUSY and SX_READY and SX != -1 and SY_READY and SY != -1 and SZ_READY and SZ != -1 and SD_READY and SD != -1 and ch == '\n')
    or
    (SIGNAL_BUSY and SX_READY and SX != -1 and SY_READY and SY != -1 and SZ_READY and SZ != -1 and SD_READY and SD != -1 and SF_READY and SF != -1 and ch == '\n')
  ):
    if (SX != -1 and SY != -1):
      move_S(SX, SY, SZ, SD, SF)
 
      ad_resetParams()
      return True
 
    else:
      ad_resetParams()
      return True
 
 
  else:
    dbgPrint("...")
    ad_resetParams()
    return True
 
 
 
 
 
 
 
def ad_manipulate_v2(line):
  
  global SX;
  global SY;
  global SZ;
  global SD;
  global SF;

  chIndex = 0
  if (len(line) <= chIndex): return False
  
  
  ch = line[chIndex]
  if (ch != '!'): return False
  
  chIndex += 1
  if (len(line) <= chIndex): return False
  
  SX = ord(line[chIndex])
  
  
  chIndex += 1
  if (len(line) <= chIndex): return False
  
  
  
  
  ch = line[chIndex]
  if (ch != '*'): return False
  
  chIndex += 1
  if (len(line) <= chIndex): return False
  
  SY__ = ord(line[chIndex])
  if (SY__ < 0):
    SY__ = 95
  elif (SY__ > 127):
    SY__ = 95

  if (SY__ < 57):
    SY__ = 57
  elif (SY__ > 124):
    SY__ = 124

  SY = SY__

  
  chIndex += 1
  if (len(line) <= chIndex): return False
  
  
  
  
  ch = line[chIndex]
  if (ch != '#'): return False
  
  chIndex += 1
  if (len(line) <= chIndex): return False
  
  SZ = ord(line[chIndex])
  
    
  chIndex += 1
  if (len(line) <= chIndex or line[chIndex] == '\n'): 
    move_S(SX, SY, SZ, -1, -1)
    return True

  
  
  ch = line[chIndex]
  if (ch != '#'): return False
  
  chIndex += 1
  if (len(line) <= chIndex): return False
  
  SD = ord(line[chIndex])
  
    
  chIndex += 1
  if (len(line) <= chIndex or line[chIndex] == '\n'):
    move_S(SX, SY, SZ, SD, -1)
    return True

  

  
  ch = line[chIndex]
  if (ch != '#'): return False
  
  chIndex += 1
  if (len(line) <= chIndex): return False
  
  SF = ord(line[chIndex])
  
  
  move_S(SX, SY, SZ, SD, SF)
  return True
    
  
 
 
 
 
 
 
ad_resetSpeed()
 
 
 
def feedStringsToBuffer(strings):
  global buffer;
  buffer += strings;
 
def feedBufferForCommand():
  global buffer;
 
  lines = buffer.splitlines(True);
  if len(lines) >= 2:
 
    # PARSE XYZ
    dbgPrint("start")
    ad_manipulate_v2(lines[-2])
    ad_resetParams()
 
  buffer = lines[-1]
  dbgPrint(lines[-1])
 
 
 
 
 
 
 
def update_mpu_data(acc, gyro, mag):
    global current_mpu_acc
    global current_mpu_gyro
    global current_mpu_mag
    current_mpu_acc = acc
    current_mpu_gyro = gyro
    current_mpu_mag = mag
 
 
 
async def server():
  global current_not_recv_server
  while True:
      dbgPrint("####### Server is listening #######")

      current_not_recv_server = True

      ready_to_read, _, _ = select.select([s], [], [], 0.5)
 
      if (ready_to_read):
        data, address = s.recvfrom(4096)
        strings = data.decode('utf-8')
        # print(strings)
        dbgPrint("\n\n A. Server received: ", strings, "\n\n")
 
        current_not_recv_server = False
 
        if strings:
          feedStringsToBuffer(strings)
        feedBufferForCommand()
 
      else:
        dbgPrint("####### Server is NOT listening #######")
        ad_resetSpeed()
        
 
 
 
 
async def multi_thread_this():
    run_multiple_tasks_at_once = await asyncio.gather(
        server(), 
    )
 
 
 
# LOOP
 
try: 
  ad_resetParams()
  ad_resetSpeed()
 
 
 
  loop = asyncio.new_event_loop()
  asyncio.set_event_loop(loop)
  loop.run_until_complete(multi_thread_this())
 
 
except KeyboardInterrupt:
 
  dbgPrint("\n\nEnding app due to keyboardinterrupt")
  ad_resetParams()
  ad_resetSpeed()
 
 
