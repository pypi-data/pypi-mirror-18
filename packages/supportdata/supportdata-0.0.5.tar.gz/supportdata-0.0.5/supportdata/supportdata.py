# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
from sys import stdout
import shutil
import hashlib
from tempfile import NamedTemporaryFile
import gzip

from six.moves.urllib.request import urlopen
from filelock import FileLock


def download_file(outputdir, url, filename=None, md5hash=None, progress=True):
    """ Download data file from a URL

        IMPROVE it to automatically extract gz files
    """
    block_size = 65536

    if not os.path.exists(outputdir):
        os.makedirs(outputdir)
    #assert os.path.exists(outputdir)

    if filename is None:
        filename = os.path.basename(url)
        if filename[-3:] == '.gz':
            filename = filename[:-3]
    fname = os.path.join(outputdir, filename)

    flock = "%s.lock" % fname
    lock = FileLock(flock)
    with lock.acquire(timeout=900):
        if os.path.isfile(fname):
            print('Already downloaded')
            return

        md5 = hashlib.md5()

        remote = urlopen(url)

        try:
            file_size = int(remote.headers["Content-Length"])
            print("Downloading: %s (%d bytes)" % (filename, file_size))
        except:
            file_size = 1e30
            print("Downloading unknown size file")

        with NamedTemporaryFile(delete=True) as f:
            bytes_read = 0
            for block in iter(lambda: remote.read(block_size), b''):
                f.write(block)
                md5.update(block)
                bytes_read += len(block)

                if progress:
                    status = "\r%10d [%6.2f%%]" % (
                            bytes_read, bytes_read*100.0/file_size)
                    stdout.write(status)
                    stdout.flush()
            if progress:
                print('')

            print(md5.hexdigest())
            if md5hash is not None:
                assert md5hash == md5.hexdigest(), \
                        "Downloaded file (%s) doesn't match expected hash (%s)" % \
                        (filename, md5.hexdigest())

            f.seek(0)
            #ext = splitext(url)[1]
            #if ext == '.gz':
            if url[-3:] == '.gz':
                with open(fname, 'wb') as fout:
                    fgz = gzip.open(f.name, 'rb')
                    for block in iter(lambda: fgz.read(block_size), ''):
                        fout.write(block)
            #elif ext == '.zip':
            #    fname = fname.replace('.zip','')
            #    with ZipFile(f.name, 'r') as zip_file:
            #        zip_file.extract(fname, data_dir)
            else:
                shutil.copy(f.name, fname)
            print("Downloaded: %s" % fname)

    #h = hash.hexdigest()
    #if h != md5hash:
    #    os.remove(f.name)
    #    print("Downloaded file doesn't match. %s" % h)
    #    assert False, "Downloaded file (%s) doesn't match with expected hash (%s)" % \
    #            (fname, md5hash)
