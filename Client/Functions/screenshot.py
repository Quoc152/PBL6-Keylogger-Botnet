import pyautogui
import os
from pynput import keyboard
import time
import threading  # Thêm thư viện threading

# Tạo đường dẫn tương đối cho thư mục Screens
screens_dir = os.path.join(os.path.dirname(__file__), '..', 'Screens')  # Đường dẫn tương đối đến thư mục Screens

# Tạo thư mục nếu chưa tồn tại
os.makedirs(screens_dir, exist_ok=True)

running = True  # Biến điều khiển vòng lặp

def on_press(key):
    global running
    try:
        if key == keyboard.Key.f12:  # Kiểm tra nếu phím F12 được nhấn
            running = False  # Dừng vòng lặp
            print("Dừng chụp ảnh màn hình.")
    except AttributeError:
        pass

def screenshot_task():
    """Chạy chức năng chụp ảnh màn hình trong một thread riêng biệt."""
    global running
    running = True 

    # Bắt đầu lắng nghe sự kiện phím
    listener = keyboard.Listener(on_press=on_press)
    listener.start()

    try:
        while running:
            # Đặt tên file ảnh với thời gian để không bị trùng
            timestamp = time.strftime("%Y%m%d_%H%M%S")  # Lấy thời gian hiện tại
            screenshot_path = os.path.join(screens_dir, f"screenshot_{timestamp}.png")  # Đường dẫn đến file ảnh

            # Chụp ảnh màn hình và lưu vào đường dẫn
            screenshot = pyautogui.screenshot()
            screenshot.save(screenshot_path) 
            print(f"Đã lưu ảnh")  # Thêm thông báo khi lưu ảnh
        
            time.sleep(5)  # Đợi 5 giây trước khi chụp ảnh tiếp theo
    except KeyboardInterrupt:
        pass
    finally:
        listener.stop() 

def start_screenshot():
    """Khởi động chức năng chụp ảnh màn hình."""
    screenshot_thread = threading.Thread(target=screenshot_task, daemon=True)
    screenshot_thread.start()  # Bắt đầu thread chụp ảnh

def stop_screenshot():
    """Dừng chức năng chụp ảnh màn hình."""
    global running
    running = False  
    print("Chức năng chụp ảnh màn hình đã dừng.")
