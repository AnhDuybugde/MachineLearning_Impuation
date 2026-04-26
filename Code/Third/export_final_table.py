import pandas as pd

# 1. Đọc và gộp 4 file CSV
files = ['ket_qua_1D.csv', 'ket_qua_3D.csv', 'ket_qua_5D.csv', 'ket_qua_7D.csv']
dfs = []

for file in files:
    df = pd.read_csv(file)
    # Làm sạch tên cột Level và Model
    df.rename(columns={df.columns[0]: 'Level', df.columns[1]: 'Model'}, inplace=True)
    df['Level'] = df['Level'].ffill()
    dfs.append(df)

df_all = pd.concat(dfs, ignore_index=True)

# 2. Loại bỏ các cột không cần thiết (Bổ sung thêm 'Time' và 'Sim')
cols_to_keep = [col for col in df_all.columns if any(metric in col for metric in ['Level', 'Model', 'MAE', 'NSE', 'R2', 'RMSE', 'Time', 'Sim'])]
df_filtered = df_all[cols_to_keep]

# 3. Tính trung bình cộng theo Level và Model
df_avg = df_filtered.groupby(['Level', 'Model']).mean(numeric_only=True).reset_index()

# Đặt lại thứ tự ưu tiên của Level: LOW -> MED -> HIGH
df_avg['Level'] = pd.Categorical(df_avg['Level'], categories=['LOW', 'MED', 'HIGH'], ordered=True)
df_avg = df_avg.sort_values(['Level', 'Model'])

# Rút gọn tên cột cho chuẩn format CSV
new_columns = []
for col in df_avg.columns:
    if 'MICE' in col and 'MAE' in col: new_columns.append('MAE_MICE')
    elif 'SICE' in col and 'MAE' in col: new_columns.append('MAE_SICE')
    elif 'MICE' in col and 'NSE' in col: new_columns.append('NSE_MICE')
    elif 'SICE' in col and 'NSE' in col: new_columns.append('NSE_SICE')
    elif 'MICE' in col and 'R2' in col: new_columns.append('R2_MICE')
    elif 'SICE' in col and 'R2' in col: new_columns.append('R2_SICE')
    elif 'MICE' in col and 'RMSE' in col: new_columns.append('RMSE_MICE')
    elif 'SICE' in col and 'RMSE' in col: new_columns.append('RMSE_SICE')
    elif 'MICE' in col and 'Time' in col: new_columns.append('Time_MICE')
    elif 'SICE' in col and 'Time' in col: new_columns.append('Time_SICE')
    elif 'MICE' in col and 'Sim' in col: new_columns.append('Sim_MICE')
    elif 'SICE' in col and 'Sim' in col: new_columns.append('Sim_SICE')
    else: new_columns.append(col)

df_avg.columns = new_columns

# 4. Xuất bảng dữ liệu ra file CSV
output_file = 'trung_binh_ket_qua.csv'
# Làm tròn 3 chữ số thập phân khi xuất file
df_avg = df_avg.round(3) 
df_avg.to_csv(output_file, index=False, encoding='utf-8')

print(f"Đã xuất dữ liệu thành công ra file: {output_file} (Bao gồm Time và Sim)")