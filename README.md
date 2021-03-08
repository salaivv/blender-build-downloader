# blender-build-downloader
A simple python script to download (or update) the latest experimental build from [builder.blender.org](https://builder.blender.org/download/).

## Usage
Put the script in the folder where you want to download the builds to and run the script. If there is no existing blender build folder in the working directory, the script will download the latest build and extract it to a folder named 'blender'. If there is already a previously downloaded build, the script will compare the timestamps and only download if necessary. 

` $ python3 ./blender_build_downloader.py`

#### Be careful not to run the script in a directory that already contains a folder named 'blender' where you store your blend files (or any other important files). The script will simply remove that folder without any warning.

#### It is best to keep and run the script in a folder solely for the blender build (to avoid accidental deletions) and pin blender to the taskbar or the dock and simply run the script daily to fetch the latest build. The same shortcuts will continue to work as long as you keep downloading to the same folder.

## Dependencies
 - [beautifulsoup4](https://pypi.org/project/beautifulsoup4/) -- used to parse html and get the download link

## Known issues
 - Downloads the wrong build when there are more than two build entries in builder.blender.org. This happens during *bcon3* when we have both a *beta* build for the upcoming release and an *alpha* build for the release after that. This also happens quite often in recent times since we now have LTS releases candidates as well. Simple workaround is to manually change the `build_num` in the script to point to the right build. A better solution would be to regex the build type directly.
 - Does not work on MacOS yet -- haven't got one to test. Though it should be very simple to do. 

## TODO
 - Make the script suggest downloading a new build when one is available. (In linux, should be pretty easy to do using `crontab` and `libnotify`. Not sure about Windows or Mac)
 - Display progress bar and network speed when downloading and extracting the archive.
 - Fix file permission error. (On Windows, sometimes python reports permission denied when renaming the extracted archive folder)
 - Try creating a UI.
