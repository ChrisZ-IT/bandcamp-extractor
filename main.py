import os
import re
from zipfile import ZipFile

def unzip_songs(start_path):
    print()
    for file in os.listdir(start_path):
        if file.endswith(".zip"):
            split_name = file.split(" - ")
            name_lengeth = len(split_name)
            artist = split_name[0].strip()
            album = ' - '.join(split_name[1:name_lengeth]).lstrip().replace(".zip","")
            destination = f"{start_path}/{artist}/{album}"
            print(f"Unzipping: {destination}")
            with ZipFile(f"{start_path}/{file}", 'r') as zObject:
                zObject.extractall(f"{destination}")
            print(f"Extracted: {destination}\n")

def rename_songs(start_path):
    pattern = r"^[0-9][0-9]\s"
    mismatch_list = []
    for root, dirs, files in os.walk(start_path):
        for file in files:
            validate_album = ""
            new_parent = ""
            rename_dir = False
            if file.endswith(".mp3"):
                split_name = file.split(" - ")
                name_lengeth = len(split_name)
                song_name = split_name[-1].lstrip()
                if name_lengeth > 1:
                    if re.search(pattern, song_name):
                        artist = root.split("/")[-2]
                        album = root.split("/")[-1]
                        validate_album = ' - '.join(split_name[1:name_lengeth - 1]).strip().lstrip().replace('.mp3','')
                        song = re.sub("(^[0-9]*)(\\s)", r"\1-", song_name)
                        rename_dir = True
                    else:
                        artist = split_name[0].strip().lstrip()
                        album = split_name[1].strip().lstrip().replace('.mp3','')
                        song = f"01-{file.split("-")[1].lstrip()}"
                    original_name = f"{root}/{file}"
                    parent_directory = f"{start_path}/{artist}/{album}"
                    new_name = f"{parent_directory}/{song}"
                    print(f"Moving: {original_name} > {new_name}")
                    os.makedirs(os.path.dirname(f"{parent_directory}/"), exist_ok=True)
                    os.rename(original_name, new_name)
                    if validate_album and validate_album != album:
                        new_parent = f"{start_path}/{artist}/{validate_album}"
                        mismatch_list.append(f"{parent_directory}>{new_parent}")
    if mismatch_list:
        correct_album_dir_name(set(mismatch_list))
    print()

def correct_album_dir_name(directory_list):
    print()
    for directory in directory_list:
        original_name = directory.split('>')[0]
        new_name = directory.split('>')[1]
        print(f"Matching dir to album name: {original_name} > {new_name}")
        os.rename(original_name, new_name)

def validate_cover_art(start_path):
    for root, dirs, files in os.walk(start_path):
        full_path = root
        album_path = root.replace(start_path,"").split('/')
        stringcount = len(album_path)
        if stringcount == 3:
            for root, dirs, files in os.walk(full_path):
                files_lower = {f.lower() for f in files}
                if not any(name in files_lower for name in ("cover.jpg", "cover.png")):
                    print(f"Missing cover art: {root}")
    print()

home = os.environ['HOME']
path = input(f"Ether Path to bandcamp downloads (default: {home}/Downloads/bandcamp): ") or f"{home}/Downloads/bandcamp"
print(f"Searching for music in: {path}\n")

# unzip_songs(path)
# rename_songs(path)
validate_cover_art(path)

print(f"Script Complete!")
print(f"Don't forget to fix song metadata!")
