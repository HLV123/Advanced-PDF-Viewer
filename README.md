# Trình Đọc Tài Liệu Nâng Cao

Ứng dụng đọc PDF hiện đại được xây dựng bằng Python, Kivy và KivyMD. Sở hữu giao diện Material Design sạch sẽ để xem tài liệu thoải mái trên tất cả các ổ đĩa hệ thống.

## Tính năng chính

- **Truy cập đa ổ đĩa**: Duyệt và mở file PDF từ bất kỳ ổ đĩa nào có sẵn
- **Điều hướng trang**: Chuyển trang bằng thanh trượt hoặc nút điều hướng
- **Điều khiển zoom**: Nút phóng to/thu nhỏ chuyên dụng với chức năng đặt lại
- **Chuyển đổi theme**: Chuyển đổi giữa giao diện sáng và tối
- **Lịch sử tài liệu**: Tự động lưu lịch sử các file gần đây
- **Giao diện responsive**: Thiết kế Material Design hiện đại với layout card
- **Đa nền tảng**: Hoạt động trên Windows, Linux và macOS

## Yêu cầu hệ thống

- Python 3.7 trở lên
- Xem file `requirements.txt` để biết các thư viện cần thiết

## Cài đặt

1. **Cài đặt các thư viện:**
```bash
pip install -r requirements.txt
```

2. **Chạy ứng dụng:**
```bash
python main.py
```

## Cấu trúc dự án

```
advanced-document-viewer/
├── main.py                    # File chính chứa logic ứng dụng
├── redesigned_interface.kv    # File giao diện Kivy
├── requirements.txt           # Danh sách thư viện cần thiết
└── README.md                  # Tài liệu hướng dẫn
```

## Hướng dẫn sử dụng

### Mở tài liệu
1. Click vào nút "Folder" trên thanh công cụ
2. Chọn ổ đĩa muốn duyệt từ dialog hiện ra
3. Tìm và chọn file PDF cần mở

### Điều hướng
- **Chuyển trang**: Sử dụng nút mũi tên trái/phải hoặc kéo thanh trượt
- **Zoom**: Click nút plus/minus để phóng to/thu nhỏ
- **Reset view**: Click nút refresh để đặt lại zoom về mặc định
- **Cuộn trang**: Sử dụng chuột hoặc thanh cuộn bên phải

### Menu bên
- Mở menu bằng cách click vào biểu tượng "menu" trên thanh tiêu đề
- Truy cập nhanh các chức năng chính
- Chuyển đổi theme sáng/tối

## Tính năng kỹ thuật

- **Hiển thị PDF**: Sử dụng PyMuPDF để render PDF với chất lượng cao
- **Giao diện Material Design**: KivyMD cung cấp các component hiện đại
- **Quản lý bộ nhớ**: Tự động đóng tài liệu cũ khi mở tài liệu mới
- **Lưu cấu hình**: Lịch sử file được lưu tự động trong thư mục user data



Nếu gặp vấn đề hoặc có đề xuất, vui lòng tạo issue trên GitHub repository.
