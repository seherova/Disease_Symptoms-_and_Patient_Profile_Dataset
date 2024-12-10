import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix, accuracy_score, classification_report
from sklearn.preprocessing import LabelEncoder
from tkinter import Tk, Label, Frame
from pathlib import Path

def show_confusion_matrix(matrix, correct, wrong, accuracy, error):
    # Initialize Tkinter
    root = Tk()
    root.title("Confusion Matrix")
    
    # Create a frame for the table
    frame = Frame(root)
    frame.pack(padx=10, pady=10)

    # Add headers
    Label(frame, text="Çıkış Değişkeni \\ Prediction (Çıkış Değişkeni)", borderwidth=1, relief="solid").grid(row=0, column=0, padx=5, pady=5)
    Label(frame, text="Positive", borderwidth=1, relief="solid").grid(row=0, column=1, padx=5, pady=5)
    Label(frame, text="Negative", borderwidth=1, relief="solid").grid(row=0, column=2, padx=5, pady=5)

    # Add confusion matrix values
    Label(frame, text="Positive", borderwidth=1, relief="solid").grid(row=1, column=0, padx=5, pady=5)
    Label(frame, text=str(matrix[0][0]), borderwidth=1, relief="solid").grid(row=1, column=1, padx=5, pady=5)
    Label(frame, text=str(matrix[0][1]), borderwidth=1, relief="solid").grid(row=1, column=2, padx=5, pady=5)
    Label(frame, text="Negative", borderwidth=1, relief="solid").grid(row=2, column=0, padx=5, pady=5)
    Label(frame, text=str(matrix[1][0]), borderwidth=1, relief="solid").grid(row=2, column=1, padx=5, pady=5)
    Label(frame, text=str(matrix[1][1]), borderwidth=1, relief="solid").grid(row=2, column=2, padx=5, pady=5)

    # Add summary stats
    Label(frame, text=f"Correct classified: {correct}", borderwidth=1).grid(row=3, column=0, columnspan=3, padx=5, pady=5, sticky="w")
    Label(frame, text=f"Wrong classified: {wrong}", borderwidth=1).grid(row=4, column=0, columnspan=3, padx=5, pady=5, sticky="w")
    Label(frame, text=f"Accuracy: {accuracy:.2f}%", borderwidth=1).grid(row=5, column=0, columnspan=3, padx=5, pady=5, sticky="w")
    Label(frame, text=f"Error: {error:.2f}%", borderwidth=1).grid(row=6, column=0, columnspan=3, padx=5, pady=5, sticky="w")
    
    # Start the Tkinter loop
    root.mainloop()

def train_simple_cart(excel_file, target_column):
    # Load the dataset
    data = pd.read_excel(excel_file)
    
    # Encode categorical columns
    label_encoders = {}
    for column in data.columns:
        if data[column].dtype == 'object' or isinstance(data[column].dtype, pd.CategoricalDtype):
            label_encoders[column] = LabelEncoder()
            data[column] = label_encoders[column].fit_transform(data[column])
    
    # Separate features and target
    X = data.drop(columns=[target_column])
    y = data[target_column]
    
    # Split into training (70%) and testing (30%) sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
    
    # Train the decision tree (SimpleCART)
    model = DecisionTreeClassifier(random_state=42)
    model.fit(X_train, y_train)
    
    # Test the model
    y_pred = model.predict(X_test)
    
    # Generate Confusion Matrix and Accuracy
    conf_matrix = confusion_matrix(y_test, y_pred)
    accuracy = accuracy_score(y_test, y_pred) * 100
    error = 100 - accuracy
    
    # Calculate correctly and falsely classified
    correctly_classified = (y_pred == y_test).sum()
    falsely_classified = (y_pred != y_test).sum()
    
    # Show confusion matrix pop-up
    show_confusion_matrix(conf_matrix, correctly_classified, falsely_classified, accuracy, error)

# Load the data
parent_path = Path(__file__).parent.parent
file_path = parent_path / 'Dönüştürülmüş_Veri.xlsx'

# Example usage
excel_file_path = file_path
target_column_name = "Çıkış Değişkeni"
train_simple_cart(excel_file_path, target_column_name)
