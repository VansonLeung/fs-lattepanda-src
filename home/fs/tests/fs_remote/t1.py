# this program is just to create an MCVE and to test the detection code. It's not an actual program.
import threading, time
from pynput.keyboard import KeyCode, Listener, Key
from pynput.mouse import Button, Controller
import asyncio
import socket
import subprocess

delay = 0.3
button = Button.right
exit_key = KeyCode(char='e')

held = 0  # declared a global. I know using globals is not a good practice. and this is just an MCVE



keymap = {}


class ClickMouse(threading.Thread):
    def __init__(self, delay, button):
        super(ClickMouse, self).__init__()
        self.delay = delay
        self.button = button
        self.running = False
        self.program_running = True

    def start_clicking(self):
        self.running = True

    def stop_clicking(self):
        self.running = False

    def exit(self):
        self.stop_clicking()
        self.program_running = False

    def run(self):
        print('about to run')
        while self.program_running:
            while self.running:
                mouse.click(self.button)
                time.sleep(self.delay)


mouse = Controller()
click_thread = ClickMouse(delay, button)
print('thread created')
click_thread.start()
print('\nthread started')


def on_press(key):
    global keymap
    if key not in keymap or keymap[key] != 1:
        keymap[key] = 1
    
        refresh_cli_status(is_update=True)
    else:
        refresh_cli_status(is_update=False)
    
    if key == exit_key:
        click_thread.exit()
        listener.stop()


def on_release(key):
    global keymap
    if key not in keymap or keymap[key] != 0:
        keymap[key] = 0
    
        refresh_cli_status(is_update=True)
    else:
        refresh_cli_status(is_update=False)


listener = Listener(on_press=on_press, on_release=on_release)
listener.start()







k_w = KeyCode(char='w')
k_s = KeyCode(char='s')
k_a = KeyCode(char='a')
k_d = KeyCode(char='d')
k_v = KeyCode(char='v')
k_b = KeyCode(char='b')
k_n = KeyCode(char='n')
k_m = KeyCode(char='m')

is_w = False
is_s = False
is_a = False
is_d = False
is_v = False
is_b = False
is_n = False
is_m = False


def refresh_cli_status(is_update):
    
    if is_update:
        global is_w
        global is_s
        global is_a
        global is_d
        global is_v
        global is_b
        global is_n
        global is_m
        
        is_w = True if (k_w in keymap and keymap[k_w] == 1) else False
        is_s = True if (k_s in keymap and keymap[k_s] == 1) else False
        is_a = True if (k_a in keymap and keymap[k_a] == 1) else False
        is_d = True if (k_d in keymap and keymap[k_d] == 1) else False
        is_v = True if (k_v in keymap and keymap[k_v] == 1) else False
        is_b = True if (k_b in keymap and keymap[k_b] == 1) else False
        is_n = True if (k_n in keymap and keymap[k_n] == 1) else False
        is_m = True if (k_m in keymap and keymap[k_m] == 1) else False
        
        # subprocess.Popen(['osascript', '-e', f'beep'])
    






UDP_IP = '127.0.0.1'  # Specify the target IP address
UDP_PORT = 8101  # Specify the target port




cs_throttle_rest = 95
cs_throttle_1_min = 89
cs_throttle_1_max = 87
cs_throttle_2_max = 85
cs_throttle_3_max = 83
cs_throttle_4_max = 81
cs_throttle_5_max = 79
cs_throttle_6_max = 77
cs_throttle_rear_min = 99
cs_throttle_rear_max = 105

cs_steering_left_max = 60
cs_steering_right_max = 120
cs_steering_center = 90

state_throttle_value = cs_throttle_rest
state_steering_value = cs_steering_center


def consume_input_and_update_state_throttle_value(delta):
    global state_throttle_value
    
    if is_w:
        if state_throttle_value > cs_throttle_1_min + 1:
            state_throttle_value = cs_throttle_1_min + 1
            
        if state_throttle_value > cs_throttle_1_max:
            state_throttle_value -= 10 * delta
            state_throttle_value = max(state_throttle_value, cs_throttle_1_max)

    elif is_s:
        if state_throttle_value < cs_throttle_rear_min:
            state_throttle_value = cs_throttle_rear_min
            
        if state_throttle_value < cs_throttle_rear_max:
            state_throttle_value += 10 * delta
            state_throttle_value = min(state_throttle_value, cs_throttle_rear_max)

    else:
        if state_throttle_value > cs_throttle_rest:
            state_throttle_value -= 50 * delta
            state_throttle_value = max(state_throttle_value, cs_throttle_rest)

        elif state_throttle_value < cs_throttle_rest:
            state_throttle_value += 50 * delta
            state_throttle_value = min(state_throttle_value, cs_throttle_rest)


def consume_input_and_update_state_steering_value(delta):
    global state_steering_value
    
    if is_a:
        if state_steering_value > cs_steering_left_max:
            state_steering_value -= 300 * delta
            state_steering_value = max(state_steering_value, cs_steering_left_max)
    
    elif is_d:
        if state_steering_value < cs_steering_right_max:
            state_steering_value += 300 * delta
            state_steering_value = min(state_steering_value, cs_steering_right_max)

    else:
        if state_steering_value > cs_steering_center:
            state_steering_value -= 300 * delta
            state_steering_value = max(state_steering_value, cs_steering_center)

        elif state_steering_value < cs_steering_center:
            state_steering_value += 300 * delta
            state_steering_value = min(state_steering_value, cs_steering_center)
       
        
def consume_input_and_update_state(delta):
    
    consume_input_and_update_state_throttle_value(delta)
    consume_input_and_update_state_steering_value(delta)
    
    print(f"\t{"w" if is_w else "_"}{"s" if is_s else "_"}{"a" if is_a else "_"}{"d" if is_d else "_"}\t{"v" if is_v else "_"}{"b" if is_b else "_"}{"n" if is_n else "_"}{"m" if is_m else "_"}\t___{get_state_steering_value_digit_1()}___\t__{get_state_throttle_value_digit_1()}.{get_state_throttle_value_digit_0_1()}__\t end", end='\r')
        


def get_state_throttle_value_digit_1():
    return int(state_throttle_value)

    
def get_state_throttle_value_digit_0_1():
    return int(round(state_throttle_value, 1) * 10) % 10


def get_state_steering_value_digit_1():
    return int(round(state_steering_value, 0))


def get_state_throttle_value_digit_0_1_as_abcdefghij():
    value = int(round(state_throttle_value, 1) * 10) % 10
    if value == 0: return ord('A')
    if value == 1: return ord('B')
    if value == 2: return ord('C')
    if value == 3: return ord('D')
    if value == 4: return ord('E')
    if value == 5: return ord('F')
    if value == 6: return ord('G')
    if value == 7: return ord('H')
    if value == 8: return ord('I')
    if value == 9: return ord('J')
    return ord('A')
    
    


def make_fs_car_message_v1():
    # legacy
    msg = f"!{chr(get_state_steering_value_digit_1())}*{chr(get_state_throttle_value_digit_1())}#{chr(90)}\n"
    return msg

def make_fs_car_message_v2():
    # 2025-02: has drift and speed fine-tune
    msg = f"!{chr(get_state_steering_value_digit_1())}*{chr(get_state_throttle_value_digit_1())}#{chr(90)}#{chr(90)}#{chr(get_state_throttle_value_digit_0_1_as_abcdefghij())}\n"
    return msg


async def send_receive_message():
    while True:
        consume_input_and_update_state(0.02)
        
        # Create a UDP socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        
        # Send a message to the specified IP address and port
        sock.sendto(make_fs_car_message_v1().encode('utf-8'), (UDP_IP, UDP_PORT))
        
        # Receive a message from the UDP socket
        # data, addr = sock.recvfrom(1024)
        
        # print(f"Received message: {data.decode()} from {addr}")
        
        await asyncio.sleep(0.02)  # Wait for 0.03 seconds before sending the next message

async def main():
    # Start the send-receive message task
    await send_receive_message()

print("\n\n")

# Run the main async function
asyncio.run(main())




    