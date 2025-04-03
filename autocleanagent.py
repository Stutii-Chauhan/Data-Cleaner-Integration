import os
import pandas as pd

# STEP 1: Install required packages
os.system('pip install gdown pydrive2')

# STEP 2: Download files from shared Google Drive folder
os.system('gdown --folder https://drive.google.com/drive/folders/1EIdJLLAmky1pMirvscMaKnzN5k8WrkGZ?usp=drive_link')

# STEP 3: Locate downloaded folder
downloaded_folder = "Mouthshut"
if not os.path.exists(downloaded_folder):
    raise Exception("Download failed or folder not found.")

# STEP 4: Create output folder
output_folder = os.path.join(downloaded_folder, "output")
os.makedirs(output_folder, exist_ok=True)

# STEP 5: List .xlsx files
xlsx_files = [f for f in os.listdir(downloaded_folder) if f.endswith('.xlsx')]
if len(xlsx_files) < 2:
    print("Not enough .xlsx files to proceed.")
    exit()

# STEP 6: Clean and save each file
columns = ['Name of Reviewer', 'Name_1', 'Location of Reviewer', 'Date of Review',
           'Views on Review', 'Title of Review', 'Detailed Review']

for file in xlsx_files:
    file_path = os.path.join(downloaded_folder, file)
    try:
        df = pd.read_excel(file_path, header=None, names=columns)
        df.drop(columns=['Name_1'], inplace=True)

        cleaned_filename = os.path.splitext(file)[0] + "_cleaned.xlsx"
        cleaned_path = os.path.join(output_folder, cleaned_filename)

        df.to_excel(cleaned_path, index=False)
        print(f"Cleaned and saved: {cleaned_filename}")

    except Exception as e:
        print(f"Failed to process {file}: {e}")

print(f"\nCleaning complete. {len(xlsx_files)} file(s) processed and saved to /Mouthshut/output.")

# STEP 7: Upload cleaned files to Google Drive
from pydrive2.auth import GoogleAuth
from pydrive2.drive import GoogleDrive

#Write the GitHub Actions secret to a file so PyDrive2 can use it
creds_path = "service_account.json"
with open(creds_path, "w") as f:
    f.write(os.environ["GDRIVE_CREDENTIALS"])

# Authenticate using service account
gauth = GoogleAuth()
gauth.LoadServiceConfigFile(creds_path)
gauth.ServiceAuth()
drive = GoogleDrive(gauth)

# Upload each cleaned file to Drive folder
folder_id = "1EIdJLLAmky1pMirvscMaKnzN5k8WrkGZ"
for file in os.listdir(output_folder):
    if file.endswith("_cleaned.xlsx"):
        file_path = os.path.join(output_folder, file)

        gfile = drive.CreateFile({
            "title": file,
            "parents": [{"id": folder_id}]
        })
        gfile.SetContentFile(file_path)
        gfile.Upload()
        print(f"Uploaded to Drive: {file}")
