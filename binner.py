import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
# Load the data
parent_path = Path(__file__).parent.parent
file_path = parent_path / 'Cleaned_Data.xlsx'
output_Path = parent_path / 'Dönüştürülmüş_Veri.xlsx'

data = pd.read_excel(file_path)

bins = [0, 20, 30, 40, 50, 60,70,80,90]  # 50'nin üstündeki değerler için ek aralık
labels = ['0-20', '21-30', '31-40', '41-50', '51-60', '61-70', '71-80', '+80']



data['Yaş_Sepetlendi'] = pd.cut(data['Yaş'], bins=bins, labels=labels, right=False)

data.to_excel(output_Path, index=False, engine='openpyxl')


# Sepetleme sonuçlarını görselleştir
age_group_counts = data['Yaş_Sepetlendi'].value_counts().sort_index()
plt.figure(figsize=(10, 6))
age_group_counts.plot(kind='bar', color='skyblue', edgecolor='black')
plt.title("Yaş Aralıklarına Göre Dağılım", fontsize=16)
plt.xlabel("Yaş Aralığı", fontsize=14)
plt.ylabel("Kişi Sayısı", fontsize=14)
plt.xticks(rotation=45, fontsize=12)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()