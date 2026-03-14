# bandcamp-extractor
Extract and organize music downloaded from bandcamp

## How it works
It will extract any albums from their zip files and organize the songs into the following directory structure/naming:
`<Artist>/<Album>/<track#>-<title>.mp3`
This script also works with singles that are not in zip files when you download them from bandcamp.
It also validates new albums are not missing album art

## How to use
1. Download all your new albums/songs
2. Move them into their own directory away from your other downloaded files (default location this script looks is `~/Downloads/bandcamp`)
3. Run script
4. Download missing album art script reports(I plan to add this part to the script)
5. Add missing metadata. bandcamp never has genre on their songs so probably that.(I also plan to automate this eventually)
