'''
Download Audio Dataset

Lei Mao

University of Chicago
'''

import os
import progressbar
from urllib.request import urlretrieve
import rarfile

pbar = None

def progress_bar(block_num, block_size, total_size):
    global pbar
    if pbar is None:

        # pbar = progressbar.ProgressBar(maxval = total_size)
        # Customized progress bar
        widgets = [progressbar.Percentage(), ' ', progressbar.Bar(marker = '>', left = '[', right = ']'), ' ', progressbar.ETA(), ' ', progressbar.FileTransferSpeed()] 
        pbar = progressbar.ProgressBar(widgets = widgets, maxval = total_size)

    downloaded = block_num * block_size
    if downloaded < total_size:
        pbar.update(downloaded)
    else:
        pbar.finish()
        pbar = None

def maybe_download(filename, url, destination_dir, expected_bytes = None, force = False):

    filepath = os.path.join(destination_dir, filename)

    if force or not os.path.exists(filepath):
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)

        print('Attempting to download: ' + filename)
        filepath, _ = urlretrieve(url, filepath, reporthook = progress_bar)
        print('Download complete!')

    statinfo = os.stat(filepath)

    if expected_bytes != None:
        if statinfo.st_size == expected_bytes:
            print('Found and verified: ' + filename)
        else:
            raise Exception('Failed to verify: ' + filename + '. Can you get to it with a browser?')
    else:
        print('Found: ' + filename)
        print('The size of the file: ' + str(statinfo.st_size))

    return filepath

'''
def maybe_unzip(zipped_filename, destination_folder, force = False):
    
    # Reference
    # https://stackoverflow.com/questions/4917284/extract-files-from-zip-without-keeping-the-structure-using-python-zipfile

    if os.path.isdir(destination_folder) and not force:
        print('%s already present - Skipping extraction of %s.' % (destination_folder.split('/')[-2], zipped_filename.split('/')[-1]))

    else:
        print("Extracting zipped file: " + zipped_filename.split('/')[-1])
        with zipfile.ZipFile(zipped_filename) as zipped_file:
            for zip_info in zipped_file.infolist():
                if zip_info.filename[-1] == '/':
                    continue
                zip_info.filename = '/'.join((zip_info.filename).split('/')[2:])
                zipped_file.extract(zip_info, destination_folder)
        print("Extraction complete!")
'''

def maybe_unrar(rarfile_dir, destination_dir, force = False):

    if os.path.isdir(destination_dir) and not force:
        print('%s already present - skipping extraction of %s' % (os.path.split(destination_dir)[-2], os.path.split(rarfile_dir)[-1]))
    else:
        print('Extracting rar file: ' + os.path.split(rarfile_dir)[-1])
        with rarfile.RarFile(rarfile_dir) as rf:
            rf.extractall(destination_dir)
        print("Extraction complete!")


def download_mir1k(download_dir = 'download/', data_dir = 'data/'):

    mir1k_url = 'http://mirlab.org/dataset/public/MIR-1K.rar'
    # Download MIR1K dataset
    mir1k_dir = maybe_download(filename = mir1k_url.split('/')[-1], url = mir1k_url, destination_dir = download_dir, force = False)
    destination_dir = os.path.join(data_dir, 'MIR1K')
    maybe_unrar(rarfile_dir = mir1k_dir, destination_dir = destination_dir, force = False)
    
    return destination_dir


if __name__ == '__main__':
    
    download_mir1k()
