import pandas as pd

# Link Google Sheets (dạng CSV xuất)
url = 'https://docs.google.com/spreadsheets/d/1e9rRiwAmRYq60Lx2PBMZcSOA8jC-rmoL/export?format=csv'

try:
    # Đọc dữ liệu từ URL
    df = pd.read_csv(url)

    # Kiểm tra kiểu dữ liệu ban đầu
    print("Kiểu dữ liệu ban đầu:")
    print(df.dtypes)

    # Chuyển cột về kiểu số, lỗi -> NaN
    df['vpv1'] = pd.to_numeric(df['vpv1'], errors='coerce')
    df['pCharge'] = pd.to_numeric(df['pCharge'], errors='coerce')
    df['SOC'] = pd.to_numeric(df['SOC'], errors='coerce')

    # Lọc dữ liệu
    filtered_df = df[(df['vpv1'] != 0) & (df['pCharge'] != 0) & (df['SOC'] > 8)]

    # Lưu file lọc
    filtered_df.to_csv('Data_new.csv', index=False)

    # Tạo cột Sum_PPV
    df['ppv1'] = pd.to_numeric(df['ppv1'], errors='coerce')
    df['ppv2'] = pd.to_numeric(df['ppv2'], errors='coerce')
    df['ppv3'] = pd.to_numeric(df['ppv3'], errors='coerce')
    df['Sum_PPV'] = df[['ppv1', 'ppv2', 'ppv3']].sum(axis=1)

    # Lưu file có Sum_PPV
    df.to_csv('Data_with_Sum_PPV.csv', index=False)

    print("✅ Đã xử lý và lưu thành công!")

except Exception as e:
    print(f"❌ Có lỗi xảy ra: {e}")
