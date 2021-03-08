# ##### BEGIN GPL LICENSE BLOCK #####
#
#  This program is free software; you can redistribute it and/or
#  modify it under the terms of the GNU General Public License
#  as published by the Free Software Foundation; either version 2
#  of the License, or (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software Foundation,
#  Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301, USA.
#
# ##### END GPL LICENSE BLOCK #####


#-----------------------------------------------------------------------------#
#                                                                             #
# blender_build_downloader.py                                                 #
#                                                                             #
# Script to download the latest blender build and extract its contents to a   #
# folder in the current directory.                                            #
#                                                                             #
# To add:                                                                     #
#     - Make script to suggest downloading a new build when one               #
#       is available.                                                         #
#     - Display progress bar and network speed when downloading and           #
#       extracting the archive.                                               #
#     - Fix file permission error.                                            #
#     - Try creating a UI.                                                    #
#                                                                             #
#-----------------------------------------------------------------------------#


import os
import re
import time
import platform
from shutil import rmtree
import urllib.request as request
from bs4 import BeautifulSoup as bs
from datetime import datetime

extension = ('.zip', '.tar.xz')

def main():
    sys_os = platform.platform()
    architecture = platform.machine()

    if sys_os.startswith('W'):
        os_name = 'os windows'
        archive_type = extension[0]
    elif sys_os.startswith('L'):
        os_name = 'os linux'
        archive_type = extension[1]

    build_num = 1

    builder_url = 'https://builder.blender.org/'
    page = request.urlopen(builder_url)

    # Get the build date and time
    soup = bs(page, 'html.parser')
    mylist = soup.findAll('li', {'class': os_name})
    build_timestamp_str = re.search('\w+\s[\d,:\s]+', \
                                mylist[build_num].small.string)
    build_timestamp_str = build_timestamp_str.group().strip()
    build_timestamp = datetime.strptime(build_timestamp_str, "%B %d, %H:%M:%S")
    build_timestamp = build_timestamp.replace(year=datetime.now().year)

    try:
        # Get the creation date of the existing blender build folder
        ts = os.stat('blender').st_ctime
        folder_timestamp = datetime.utcfromtimestamp(ts)
        EXISTS = 1

        # Check if the latest build is already in place
        if folder_timestamp > build_timestamp:
            print("\n Latest build already in place.")
            time.sleep(5)
            return
    except FileNotFoundError:
        print('\n No existing blender build folder found.')
        EXISTS = 0

    page_src = str(page.read())
    link = soup.findAll('li', {'class': os_name})[build_num].a['href']
    download_url = builder_url + link

    print("\n Download link found: " + download_url + '\n')

    if EXISTS:
        print(' Removing the old directory...')
        rmtree('blender')
        print(' Removed the old directory.\n')
    
    archive = 'blender' + archive_type
    
    # Check if a build archive already exists
    if os.path.exists(archive):
        archive_ts = os.stat(archive).st_ctime
        archive_timestamp = datetime.utcfromtimestamp(archive_ts)

        # If the latest archive is already available, do not download, else
        # remove the existing archive and download the latest one.
        if archive_timestamp > build_timestamp:
            print(" Latest build archive already in place.\n")
        else:
            os.remove(archive)
            print(' Downloading...')
            request.urlretrieve(download_url, archive)
            print(' Download complete.\n')
    else:
        print(' Downloading...')
        request.urlretrieve(download_url, archive)
        print(' Download complete.\n')

    print(' Extracting files...')
    
    if archive_type == '.zip':
        import zipfile
        with zipfile.ZipFile(archive, 'r') as f:
            f.extractall('./')
    else:
        import tarfile
        with tarfile.open(archive, 'r') as f:
            f.extractall('./')  
    print(' Finished exracting.\n')

    for i in os.listdir('./'):
        if i.startswith('blender-'):
            if os.path.isdir(i):
                directory = i

    os.rename(directory, 'blender')

    print(' Removing the archive...')
    os.remove(archive)
    print(' Done.\n')
    time.sleep(5)

if __name__ == '__main__':
    main()
