import os

from tools import toolbox


def clean_files() -> None:
    """Removes all duplicates in the resources"""
    tools = toolbox.Toolbox()
    resources = tools.get_data_directory()

    for filename in os.listdir(resources):
        with open(resources + filename, 'r+') as file:
            lines = file.readlines()

            # Delete file contents
            file.seek(0)
            file.truncate()

            # Remove duplicates, sort them alphabetically
            cleaned_lines = sorted(list(set(lines)))
            file.writelines(cleaned_lines)


if __name__ == '__main__':
    clean_files()
