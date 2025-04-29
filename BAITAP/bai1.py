import requests
import csv
from datetime import datetime

def fetch_weather_data():
    # URL API thời tiết
    url = "https://api.open-meteo.com/v1/forecast?latitude=52.52&longitude=13.41&past_days=10&hourly=temperature_2m,relative_humidity_2m,wind_speed_10m"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print("Lỗi khi lấy dữ liệu từ API:", response.status_code)
        return None

def save_to_csv(data, filename="weather_data.csv"):
    try:
        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            # Ghi tiêu đề cột
            writer.writerow(["latitude", "longitude", "time", "temperature_2m", "relative_humidity_2m", "wind_speed_10m"])
            # Ghi dữ liệu vào file
            for i, time in enumerate(data["hourly"]["time"]):
                writer.writerow([
                    data["latitude"], 
                    data["longitude"], 
                    time, 
                    data["hourly"]["temperature_2m"][i], 
                    data["hourly"]["relative_humidity_2m"][i], 
                    data["hourly"]["wind_speed_10m"][i]
                ])
        print(f"Dữ liệu đã được lưu vào file {filename}")
    except Exception as e:
        print("Lỗi khi lưu dữ liệu vào CSV:", e)

def calculate_totals(filename="weather_data.csv", end_date="2025-04-29"):
    try:
        total_temperature = 0
        total_humidity = 0
        total_wind_speed = 0
        
        end_date = datetime.strptime(end_date, "%Y-%m-%d")
        with open(filename, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Chuyển đổi thời gian và kiểm tra ngày
                date = datetime.strptime(row["time"], "%Y-%m-%dT%H:%M")
                if date.date() <= end_date.date():
                    total_temperature += float(row["temperature_2m"])
                    total_humidity += float(row["relative_humidity_2m"])
                    total_wind_speed += float(row["wind_speed_10m"])
        
        print("Tổng giá trị:")
        print(f"- Tổng nhiệt độ: {total_temperature}")
        print(f"- Tổng độ ẩm: {total_humidity}")
        print(f"- Tổng tốc độ gió: {total_wind_speed}")
    except Exception as e:
        print("Lỗi khi tính toán tổng giá trị:", e)

# Thực hiện các bước
data = fetch_weather_data()
if data:
    save_to_csv(data)
    calculate_totals()
