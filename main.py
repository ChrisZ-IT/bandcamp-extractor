import os
import re
import requests
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
    for root, dirs, files in os.walk(start_path):
        for file in files:
            if file.endswith(".mp3"):
                album_match = re.match(
                    r"^(.*?)\s-\s(.*?)\s-\s([0-9]{2}\s.*\.mp3)$",
                    file
                )

                if album_match:
                    artist = album_match.group(1)
                    album = album_match.group(2)
                    filename = album_match.group(3)
                else:
                    single_match = re.match(r"^(?!\d{2}-)(.*?)\s-\s(.+\.mp3)$", file)
                    if single_match:
                        artist = single_match.group(1)
                        album = single_match.group(2).replace('.mp3','')
                        filename = f"01 {single_match.group(2)}"
                if album_match or single_match:
                    parent_directory = os.path.join(start_path, artist, album)
                    song = re.sub("(^[0-9]*)(\\s)", r"\1-", filename)
                    original_name = os.path.join(root, file)
                    new_name = f"{parent_directory}/{song}"
                    print(f"Moving:\n\t{original_name} -->\n\t{new_name}\n")
                    os.makedirs(os.path.dirname(f"{parent_directory}/"), exist_ok=True)
                    os.rename(original_name, new_name)
    print()

def correct_cover_art(start_path):
    for root, dirs, files in os.walk(start_path):
        regex_string = "(?i)^(folder|cover)"
        full_path = root
        album_path = root.replace(start_path,"").split('/')
        stringcount = len(album_path)
        if stringcount == 3:
            for root, dirs, files in os.walk(full_path):
                for file in files:
                    if (file.endswith(".png") or file.endswith(".jpg")):
                        if (re.search(regex_string, file)):
                            file_ext = file.split('.')[-1]
                            original_name = f"{root}/{file}"
                            new_name = f"{root}/cover.{file_ext}"
                            if original_name != new_name:
                                print(f"Renaming: {original_name} --> {new_name}")
                                os.rename(original_name, new_name)
    print()

def get_album_id(artist, album):
    url = "https://musicbrainz.org/ws/2/release/"

    params = {
        "query": f'artist:"{artist}" AND release:"{album}"',
        "fmt": "json",
        "limit": 1
    }

    headers = {
        "User-Agent": "MyAlbumArtApp/1.0 (admin@musicbrainz.org)"
    }

    response = requests.get(url, params=params, headers=headers)
    response.raise_for_status()

    data = response.json()

    release = data["releases"][0]

    return (release["id"])

def download_album_art(mbid,output_path):

    url = f"https://coverartarchive.org/release/{mbid}"

    response = requests.get(url)
    response.raise_for_status()

    cover_data = response.json()

    front = next(
        img for img in cover_data["images"]
        if img["front"]
    )

    thumbnails = front.get("thumbnails", {})

    image_url = (
        thumbnails.get("1200")
        or thumbnails.get("large")
        or front["image"]
    )

    img = requests.get(image_url)
    img.raise_for_status()

    with open(f"{output_path}/cover.jpg", "wb") as f:
        f.write(img.content)

    print(f"Downloaded {output_path}/cover.jpg. Validate it is correct")

def validate_cover_art(start_path):
    for root, dirs, files in os.walk(start_path):
        full_path = root
        album_path = root.replace(start_path,"").split('/')
        stringcount = len(album_path)
        if stringcount == 3:
            artist = album_path[1]
            album = album_path[2]
            for root, dirs, files in os.walk(full_path):
                files_lower = {f.lower() for f in files}
                if not any(name in files_lower for name in ("cover.jpg", "cover.png")):
                    mbid = get_album_id(artist, album)
                    if mbid:
                        print(f"{artist}/{album}: Missing cover art. Attempting to locate and download it")
                        download_album_art(mbid,root)
                    else:
                        print(f"Unable to find cover art: {root}")
    print()

home = os.environ['HOME']
path = input(f"Ether Path to bandcamp downloads (default: {home}/Downloads/bandcamp): ") or f"{home}/Downloads/bandcamp"
print(f"Searching for music in: {path}\n")

unzip_songs(path)
rename_songs(path)
correct_cover_art(path)
validate_cover_art(path)

print(f"Script Complete!")
print(f"Don't forget to fix song metadata!")
