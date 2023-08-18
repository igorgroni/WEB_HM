import sys
import os
import re
import shutil
import zipfile


def main():

    def normalize(name):
        translit_dict = {
            'а': 'a', 'б': 'b', 'в': 'v', 'г': 'h', 'ґ': 'g', 'д': 'd', 'е': 'e', 'є': 'ie', 'ж': 'zh', 'з': 'z',
            'и': 'y', 'і': 'i', 'ї': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p',
            'р': 'r', 'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
            'ь': '', 'ю': 'iu', 'я': 'ia',
            'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'H', 'Ґ': 'G', 'Д': 'D', 'Е': 'E', 'Є': 'IE', 'Ж': 'ZH', 'З': 'Z',
            'И': 'Y', 'І': 'I', 'Ї': 'I', 'Й': 'I', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P',
            'Р': 'R', 'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'KH', 'Ц': 'TS', 'Ч': 'CH', 'Ш': 'SH', 'Щ': 'SHCH',
            'Ь': '', 'Ю': 'IU', 'Я': 'IA'
        }

        translit_name = ''.join(translit_dict.get(char, char) for char in name)

        normalized_name = re.sub(r'[^A-Za-z0-9]', '_', translit_name)

        return normalized_name

    def rename_files_and_folders(folder_path):
        for item in os.listdir(folder_path):
            item_path = os.path.join(folder_path, item)
            if os.path.isfile(item_path):
                filename, file_extension = os.path.splitext(item)
                normalized_name = normalize(filename) + file_extension
                new_item_path = os.path.join(folder_path, normalized_name)
                os.rename(item_path, new_item_path)
            elif os.path.isdir(item_path):
                rename_files_and_folders(item_path)

    def sort_files_by_format(folder_path):
        formats = {
            'Images': ['.jpg', '.jpeg', '.png', '.gif'],
            'Documents': ['.doc', '.docx', '.txt', '.pdf'],
            'Videos': ['.mp4', '.avi', '.mkv'],
            'Audio': ['.mp3', '.wav', '.flac'],
            'archives': ['.zip']
        }

        ignored_folders = ['archives', 'Videos',
                           'Audio', 'Documents', 'Images']
        folders = ['Videos', 'Audio', 'Documents', 'Images']

        # Обходим все файлы в папке
        for filename in os.listdir(folder_path):
            file_path = os.path.join(folder_path, filename)

            for folder_name in folders:
                destination_folder = os.path.join(folder_path, folder_name)
                print(destination_folder)

                if not os.path.exists(destination_folder):
                    os.makedirs(destination_folder)
                    print(f"Создана папка: {destination_folder}")
                else:
                    print(f"Папка уже существует: {destination_folder}")

            # перевіряєм чи являє собою файл
            if os.path.isfile(file_path):

                for folder_name, extensions in formats.items():
                    # Встановлюємо формат файлу
                    file_extension = os.path.splitext(filename)[1].lower()

                    if file_extension in extensions:
                        destination_folder = os.path.join(
                            folder_path, folder_name)
                        if file_extension in ['.jpg', '.jpeg', '.png', '.gif']:
                            shutil.move(file_path, os.path.join(
                                destination_folder, filename))

                        elif file_extension in ['.mp4', '.avi', '.mkv']:
                            shutil.move(file_path, os.path.join(
                                destination_folder, filename))

                        elif file_extension in ['.doc', '.docx', '.txt', '.pdf']:
                            shutil.move(file_path, os.path.join(
                                destination_folder, filename))

                        elif file_extension in ['.mp3', '.wav', '.flac']:
                            shutil.move(file_path, os.path.join(
                                destination_folder, filename))

                        elif file_extension in ['.zip']:
                            extract_folder = os.path.join(
                                folder_path, 'archives', os.path.splitext(filename)[0])
                            os.makedirs(extract_folder, exist_ok=True)

                            with zipfile.ZipFile(file_path, 'r') as zip_ref:
                                zip_ref.extractall(extract_folder)

                            os.remove(file_path)

                        else:
                            break

            elif os.path.isdir(file_path):
                # Рекурсивно викликаємо функцію для вкладеної папки
                sort_files_by_format(file_path)

        for folder_name in os.listdir(folder_path):
            folder = os.path.join(folder_path, folder_name)
            if os.path.isdir(folder) and folder_name not in ignored_folders and not os.listdir(folder):
                os.rmdir(folder)

        print("Сортировка файлов завершена.")

    if len(sys.argv) < 2:
        print("Потрібно вказати шлях до папки для сортування.")
        sys.exit(1)

    folder_path = sys.argv[1]
    rename_files_and_folders(folder_path)
    sort_files_by_format(folder_path)
