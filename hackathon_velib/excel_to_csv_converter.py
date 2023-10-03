import os
import pandas as pd

class DataProcessor:
    def __init__(self, base_folder, excel_folder, csv_folder):
        self.base_folder = base_folder
        self.excel_folder = excel_folder
        self.csv_folder = csv_folder

    def read_excel_files(self, folder_path):
        dataframes = []
        # Parcourir les fichiers Excel
        for file_name in os.listdir(folder_path):
            if file_name.endswith(".xlsx"):
                file_path = os.path.join(folder_path, file_name)

                # Lire le fichier Excel dans un DataFrame
                df = pd.read_excel(file_path)

                # Ajouter le DataFrame à la liste
                dataframes.append(df)
        return dataframes

    def export_to_csv(self, dataframe, csv_file_name):
        # Chemin pour sauvegarder le fichier CSV
        output_csv_path = os.path.join(self.csv_folder, csv_file_name)

        # Sauvegarder le DataFrame en tant que fichier CSV
        dataframe.to_csv(output_csv_path, index=False)

        print(f"Fichier CSV créé : {output_csv_path}")

    def process_data(self):
        # Parcourir chaque sous-dossier numéroté 0X_Nom_du_dossier
        for folder_name in os.listdir(self.excel_folder):
            if folder_name.startswith("0") and os.path.isdir(os.path.join(self.excel_folder, folder_name)):
                # Parcourir les sous-dossiers 2023_02 et 2023_06
                for subfolder_name in ["2023_02", "2023_06"]:
                    subfolder_path = os.path.join(self.excel_folder, folder_name, subfolder_name)
                    if os.path.exists(subfolder_path) and os.path.isdir(subfolder_path):
                        # Liste pour stocker les données de chaque jour
                        dataframes = self.read_excel_files(subfolder_path)

                        # Concaténer les DataFrames en un seul
                        combined_df = pd.concat(dataframes)

                        # Nom du fichier CSV basé sur le dossier parent et la période correspondante
                        csv_file_name = f"{subfolder_name}_{folder_name}.csv"

                        # Exporter le DataFrame combiné au format CSV
                        self.export_to_csv(combined_df, csv_file_name)

# Chemin du dossier principal contenant les données
base_folder = "./data"

# Chemin du dossier contenant les fichiers Excel
excel_folder = os.path.join(base_folder, "excel")

# Chemin du dossier où enregistrer les fichiers CSV
csv_folder = os.path.join(base_folder, "csv")

# Créer le dossier CSV s'il n'existe pas
if not os.path.exists(csv_folder):
    os.makedirs(csv_folder)

# Créer une instance de la classe DataProcessor et appeler la méthode process_data
data_processor = DataProcessor(base_folder, excel_folder, csv_folder)
data_processor.process_data()
