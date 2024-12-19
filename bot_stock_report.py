import os
import gspread
from telegram import Bot
from dotenv import load_dotenv
from oauth2client.service_account import ServiceAccountCredentials

TELEGRAM_TOKEN=7679871351:AAHWmsq-PrvpFRByFtsCU4bMunM0gFEHH7E
CHAT_ID=YOUR_CHAT_ID
SHEET_URL=https://docs.google.com/spreadsheets/d/11IS8ynBC4D5pk2OmDtBNmGcobpuWWI-BWwjrwpfldFk/edit#gid=0

# ====== CẤU HÌNH ======
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")
SHEET_URL = os.getenv("SHEET_URL")
GOOGLE_CREDENTIALS_FILE = "credentials.json"  # Đường dẫn file JSON (thêm vào dự án)

# ====== KẾT NỐI GOOGLE SHEETS ======
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name(GOOGLE_CREDENTIALS_FILE, scope)
client = gspread.authorize(creds)

# Mở Google Sheets
sheet = client.open_by_url(SHEET_URL)
worksheet = sheet.get_worksheet(0)  # Lấy sheet đầu tiên

# ====== ĐỌC DỮ LIỆU ======
data = worksheet.get_all_values()  # Đọc toàn bộ dữ liệu
headers = data[0]  # Dòng tiêu đề
rows = data[1:]  # Các dòng dữ liệu

# ====== TẠO NỘI DUNG BẢN TIN ======
def create_report(rows):
    report = "📊 *Báo cáo thị trường chứng khoán*\n\n"
    vn_index_row = rows[4]  # Hàng VNIndex (thay bằng hàng tương ứng)
    report += f"- VN-Index đóng cửa: {vn_index_row[1]} điểm\n"
    report += f"- Tăng/Giảm trong phiên: {vn_index_row[5]} điểm\n"
    report += f"- Tổng giá trị giao dịch: {vn_index_row[11]} tỷ VNĐ\n\n"
    
    # Top cổ phiếu nổi bật
    report += "🌟 *Các cổ phiếu nổi bật hôm nay:*\n"
    for row in rows[:3]:  # Lấy Top 3 cổ phiếu
        report += f"  - {row[0]}: {row[5]} điểm, khối lượng: {row[10]} cổ phiếu\n"
    
    return report

report = create_report(rows)

# ====== GỬI TIN NHẮN QUA TELEGRAM ======
bot = Bot(token=TELEGRAM_TOKEN)
bot.send_message(chat_id=CHAT_ID, text=report, parse_mode="Markdown")
