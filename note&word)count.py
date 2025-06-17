import os

def count_files_and_words(directory):
    file_count = 0
    total_words = 0

    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".md"):  # Assuming you are working with Markdown files
                file_count += 1
                with open(os.path.join(root, file), 'r', encoding='utf-8') as f:
                    content = f.read()
                    total_words += len(content.split())

    return file_count, total_words

directory = "C:/Users/adamm/Nihilismi Experientia Sacra"
file_count, total_words = count_files_and_words(directory)
print(f"Number of files: {file_count}")
print(f"Total word count: {total_words}")