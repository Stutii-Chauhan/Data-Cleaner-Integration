import os
import pandas as pd

# STEP 1: Download files from the shared Google Drive folder
os.system('pip install gdown')
os.system('gdown --folder https://drive.google.com/drive/folders/1EIdJLLAmky1pMirvscMaKnzN5k8WrkGZ?usp=drive_link')

# STEP 2: Locate downloaded folder
downloaded_folder = "1EIdJLLAmky1pMirvscMaKnzN5k8WrkGZ"
if not os.path.exists(downloaded_folder):
    raise Exception("Download failed or folder not found.")

# STEP 3: List .xlsx files
xlsx_files = [f for f in os.listdir(downloaded_folder) if f.endswith('.xlsx')]
if len(xlsx_files) < 2:
    print("Not enough .xlsx files to proceed.")
    exit()

# STEP 4: Clean each file
columns = ['Name of Reviewer', 'Name_1', 'Location of Reviewer', 'Date of Review',
           'Views on Review', 'Title of Review', 'Detailed Review']

for file in xlsx_files:
    file_path = os.path.join(downloaded_folder, file)
    try:
        df = pd.read_excel(file_path, header=None, names=columns)
        df.drop(columns=['Name_1'], inplace=True)
        
        var_name = os.path.splitext(file)[0].replace(" ", "_").lower() + "_df"
        globals()[var_name] = df
        
        print(f"Created DataFrame: {var_name}")
    except Exception as e:
        print(f"Failed to process {file}: {e}")

print(f"Cleaning complete. {len(xlsx_files)} file(s) processed.")
