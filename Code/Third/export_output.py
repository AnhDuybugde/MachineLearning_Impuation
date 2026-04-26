import json
import pandas as pd

# Đọc nội dung file Jupyter Notebook
notebook_path = 'mice-sice.ipynb'
with open(notebook_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

tables = []

# Duyệt qua các cell để tìm output chứa bảng dữ liệu (định dạng HTML từ Pandas)
for cell in nb.get('cells', []):
    if cell.get('cell_type') == 'code':
        for output in cell.get('outputs', []):
            if 'data' in output and 'text/html' in output['data']:
                html_content = "".join(output['data']['text/html'])
                try:
                    # Đọc bảng HTML thành DataFrame
                    df = pd.read_html(html_content)[0]
                    tables.append(df)
                except Exception as e:
                    continue

# Giả định 4 bảng cuối cùng trong output là kết quả của 1D, 3D, 5D, 7D
days = ['1D', '3D', '5D', '7D']
target_tables = tables[-4:] 

if len(target_tables) == 4:
    for i, df in enumerate(target_tables):
        # Làm phẳng và dọn dẹp tên cột MultiIndex
        if isinstance(df.columns, pd.MultiIndex):
            new_cols = []
            for col in df.columns.values:
                # Bỏ qua các chuỗi "Unnamed" do merge cell tạo ra
                col_str = "_".join([str(c) for c in col if "Unnamed" not in str(c)])
                
                # Cấu trúc lại tên cột cho đồng nhất và dễ truy xuất
                if "Level" in col_str: name = "Level"
                elif "Model" in col_str: name = "Model"
                elif "MAE" in col_str and "MICE" in col_str: name = "MAE_MICE"
                elif "MAE" in col_str and "SICE" in col_str: name = "MAE_SICE"
                elif "NSE" in col_str and "MICE" in col_str: name = "NSE_MICE"
                elif "NSE" in col_str and "SICE" in col_str: name = "NSE_SICE"
                elif "R2" in col_str and "MICE" in col_str: name = "R2_MICE"
                elif "R2" in col_str and "SICE" in col_str: name = "R2_SICE"
                elif "RMSE" in col_str and "MICE" in col_str: name = "RMSE_MICE"
                elif "RMSE" in col_str and "SICE" in col_str: name = "RMSE_SICE"
                elif "Sim" in col_str and "MICE" in col_str: name = "Sim_MICE"
                elif "Sim" in col_str and "SICE" in col_str: name = "Sim_SICE"
                elif "Time" in col_str and "MICE" in col_str: name = "Time_MICE"
                elif "Time" in col_str and "SICE" in col_str: name = "Time_SICE"
                else: name = col_str # Giữ nguyên nếu không khớp định dạng
                
                new_cols.append(name)
                
            df.columns = new_cols
            
        # Lấp đầy các giá trị NaN ở cột Level (do merge cells trong HTML)
        if 'Level' in df.columns:
            df['Level'] = df['Level'].ffill()
            
        # Xuất ra file CSV
        filename = f"ket_qua_{days[i]}.csv"
        df.to_csv(filename, index=False)
        print(f"Đã xuất thành công: {filename} (Đã bao gồm cột Time và Sim)")
else:
    print(f"Tìm thấy {len(tables)} bảng, vui lòng kiểm tra lại cấu trúc output trong file.")