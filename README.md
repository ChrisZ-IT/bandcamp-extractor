# bandcamp-extractor
Extract and organize music downloaded from bandcamp

## How it works
It will extract any albums from their zip files and organize the songs into the following directory structure/naming:
`<Artist>/<Album>/<track#>-<title>.<file_extension>`


- Also works with singles that are not in zip files.

- Ensures cover art is consistently named `cover.<file_extension>`

- If albums are missing cover art it will attempt to look the album up on musicbrainz.org and then download the art from coverartarchive.org. If that fails it will alert you to manually add cover art.

## How to use
1. Download all your new albums/songs
2. Move them into their own directory away from your other downloaded files (default location this script looks is `~/Downloads/bandcamp`)
3. Run script
4. Download any cover art it cant find
5. Add missing metadata. Bandcamp never has genre on their songs :(
    - Will try and get this added to a future release of this script.
