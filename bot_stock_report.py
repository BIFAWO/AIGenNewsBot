import requests
from telegram import Bot

# ===== CẤU HÌNH =====
TELEGRAM_TOKEN = "7679871351:AAHWmsq-PrvpFRByFtsCU4bMunM0gFEHH7E"
CHAT_ID = "YOUR_CHAT_ID"  # Thay bằng Chat ID của bạn
SHEET_ID = "11IS8ynBC4D5pk2OmDtBNmGcobpuWWI-BWwjrwpfldFk"
SHEET_NAME = "Dashboard"  # Tên sheet chính

# ===== LẤY DỮ LIỆU TỪ GOOGLE SHEETS =====
def get_sheet_data(sheet_id, sheet_name):
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={sheet_name}"
    response = requests.get(url)
    response.raise_for_status()  # Báo lỗi nếu request thất bại
    data = response.text
    rows = [row.split(",") for row in data.split("\n") if row]
    return rows

# Đọc dữ liệu từ Google Sheets
data = get_sheet_data(SHEET_ID, SHEET_NAME)

# ===== TẠO NỘI DUNG BẢN TIN =====
def create_report(data):
    vn_index_row = data[5]  # Lấy dòng VNIndex (thay đổi theo cấu trúc bảng của bạn)
    report = f"📊 *Thị trường chứng khoán hôm nay*\n\n"
    report += f"VN-Index: {vn_index_row[1]} điểm, thay đổi: {vn_index_row[5]} điểm\n"
    report += f"Tổng giá trị giao dịch: {vn_index_row[11]} tỷ VNĐ\n\n"
    
    # Top cổ phiếu nổi bật
    report += "🌟 *Cổ phiếu nổi bật:*\n"
    for row in data[:3]:  # Lấy top 3 cổ phiếu (thay đổi nếu cần)
        report += f"- {row[0]}: {row[5]} điểm, khối lượng: {row[10]} cổ phiếu\n"
    return report

report = create_report(data)

# ===== GỬI TIN NHẮN QUA TELEGRAM =====
bot = Bot(token=TELEGRAM_TOKEN)
bot.send_message(chat_id=CHAT_ID, text=report, parse_mode="Markdown")
