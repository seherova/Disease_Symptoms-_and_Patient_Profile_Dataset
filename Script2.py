import pandas as pd
from sklearn.metrics import accuracy_score

file_path = "/Users/seherova/Downloads/FinalOdevi/Cleaned_Data.xlsx"
df = pd.read_excel(file_path)
target_column = 'Çıkış Değişkeni'

def zero_r(df, target_column):
    most_common_class = df[target_column].mode()[0]
    
    predictions = [most_common_class] * len(df)
    return most_common_class, predictions

most_common_class, predictions = zero_r(df, target_column)

true_values = df[target_column].tolist()
accuracy = accuracy_score(true_values, predictions)

print(f"En yaygın değişken (zeroR): {most_common_class}")
print(f"ZeroR doğruluk skoru: {accuracy:.2f}")