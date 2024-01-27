# We must remove the first line and the line which have [Refrain], [Couplet], ...

import os
from tqdm import tqdm


def change_file(file_path: str) -> None:
    file = []
    new_file = []

    # Open file
    with open(file_path, mode='r', encoding='utf8') as f:
        for line in f.readlines():
            file.append(line[:-1])
        f.close()
    
    # remove first line
    if 'Contributors' in file[0]:
        file = file[1:]

    # remove empty line and line with [Refrain], [Couplet], ...
    for line in file:
        if len(line) > 0 and not(line[0] == '['):
            new_file.append(line)

    # Remove 1Embe at the end
    if '1Embe' in new_file[-1]:
        new_file[-1] = new_file[-1][:-5]
    
    # Save file
    with open(file_path, mode='w', encoding='utf8') as f:
        for line in new_file:
            f.write(line + '\n')
        f.close()


if __name__ == '__main__':
    path = os.path.join('..', 'data', 'genius_lyrics')
    for artit in os.listdir(path):
        for file in os.listdir(os.path.join(path, artit)):
            print(artit, ':', file)
            change_file(os.path.join(path, artit, file))

