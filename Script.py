import pandas as pd
from pathlib import Path
import seaborn as sns
import matplotlib.pyplot as plt
# Load the data
parent_path = Path(__file__).parent.parent
file_path = parent_path / 'Data_With_Nonsense_Values.xlsx'
output_Path = parent_path / 'Cleaned_Data.xlsx'

data = pd.read_excel(file_path)

print('Veri bilgisi:')
print(data.info(), "\n")              

print("Temel İstatistikler:")
summary_stats = data.describe(include="all").transpose()
print(summary_stats.to_string())

#for col in data.columns:
#print(f"{col} unique values:", data[col].unique())

# Count missing values in each column
print('Eksik Değerler:')
missing_values = data.isnull().sum()
print(missing_values[missing_values > 0].to_string()) #sadece eksik değerleri yazdır

# Drop rows with missing values
data_cleaned = data.dropna()

data_cleaned.to_excel(output_Path, index=False) #output_Path'e geçirdim


# Example: Remove rows where "age" is negative or above 120
#valid_age_mask = (data_cleaned['Yaş'] >=0) & (data_cleaned['Yaş'] <=120)
#data_cleaned = data_cleaned[valid_age_mask]

data_cleaned = data_cleaned[(data_cleaned['Yaş'] >= 0) & (data_cleaned['Yaş'] <= 120)]
data_cleaned.to_excel(output_Path, index=False)


# Validate binary columns (e.g., "positive" or "negative")
valid_values = ['Male', 'Female']
data_cleaned = data_cleaned[data_cleaned['Cinsiyet'].isin(valid_values)]

data_cleaned.to_excel(output_Path, index=False)


# OUTLIER DETECTION, Tamamlanmadı, bizim veri setinde numerik outlier olması için bir satır daha eklemek lazım sadece yaş sütunu Outlier olan.
# IQR method for outlier detection
multiplier = 1.5 
Q1 = data_cleaned['Yaş'].quantile(0.25)
Q3 = data_cleaned['Yaş'].quantile(0.75)
IQR = Q3 - Q1

# z score ile de yapılabilir.
# asymmetric distrubution (gauss dağılımda)
# outlier'da uzman görüşüne dayanmak

# Remove outliers
data_cleaned = data_cleaned[~((data_cleaned['Yaş'] < (Q1 - multiplier * IQR)) | (data_cleaned['Yaş'] > (Q3 + multiplier * IQR)))]

# Save the cleaned data to a new Excel file
data_cleaned.to_excel(output_Path, index=False)
print(f"\n###Temizlenmiş veri kaydedildi:{output_Path}###")

#binary_columns = ["Ateş", "Öksürük", "Yorgunluk", "Nefes Almada Zorluk", "Cinsiyet", "Çıkış Değişkeni", "Kan Basıncı", "Kolesterol Seviyesi"]

# binary_map = {
    # 'Yes':1, 'No':0,
    # # 'Male': 1, 'Female': 0,
    # 'Positive':1, 'Negative': 0,
    # 'Low': -1, 'Normal':0, 'High':1
# }
#                                   **gereksiz nitelikler için korelasyon anlamlı**
# 

df_encoded = data_cleaned.copy()

for col in binary_columns:
   df_encoded[col] = data_cleaned[col].map(binary_map)

output_file = parent_path / "encoded_data.xlsx"
df_encoded.to_excel(output_file, index=False)
print(f"Kodlanmış veri {output_file} dosyasına kaydedildi")

correlation_matrix = df_encoded[binary_columns].corr()

print("Korelasyon matrisi")
print(correlation_matrix)

plt.figure(figsize=(10, 8))
sns.heatmap(correlation_matrix, annot=True, cmap="coolwarm", cbar=True)
plt.title("Korelasyon Matrisi Isı Haritası")
plt.show()

