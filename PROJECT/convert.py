import pandas as pd

# Load the CSV you already have
df = pd.read_csv(r"C:\Users\kkhan\Downloads\Comprehensive_Athlete_Nutrition_Dataset.csv")

# Extract that paragraph column and drop any empty rows
text_lines = df['RAG_Context'].dropna().tolist()

# Save it as a plain text document
with open('Athlete_Nutrition_Data.txt', 'w', encoding='utf-8') as f:
    for line in text_lines:
        f.write(line + "\n\n")

print("Success! Athlete_Nutrition_Data.txt has been created in your folder.")