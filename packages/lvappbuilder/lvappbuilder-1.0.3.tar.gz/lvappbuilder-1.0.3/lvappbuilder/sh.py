import shutil
import os
import re

def ls(location='.', pattern='.*'):
    """Return files and directories in given location.
       pattern - regexp that specifies filter to be applied.
    """
    file_list = []
    for (dirpaths, dirnames, filenames) in os.walk(location):
        for filename in dirnames + filenames:
            if re.match(pattern, filename):
                file_list.append(filename)
    return file_list
    
def rm(target):
    """Remove given file or directory recursively. If path is invalid, simply do nothing.
    """
    if os.path.isdir(target) and not os.path.islink(target):
        shutil.rmtree(target)
    elif os.path.exists(target):
        os.remove(target)
        
def replace_in_file(filepath, phrase, sub):
    """Replace all occurrences of given phrase in file.
    """
    text = open(filepath).read().replace(phrase, sub)
    open(filepath, 'w').write(text)
    
def backup(filepath):
    """Backup file or directory.
    """
    shutil.copy(filepath, filepath+'.bkp')

def restore(filepath):
    """Restore file or directory from backup and remove backup.
    """
    shutil.move(filepath+'.bkp', filepath)
