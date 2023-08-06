import platform
import xmltodict
import psutil
from path import Path
from subprocess import Popen
from collections import OrderedDict
from retrying import retry
from regobj import HKEY_LOCAL_MACHINE as HKLM
from .filterable import Filterable

LOCAL_DIR_PATH = Path(__file__).abspath().parent
EXIT_VI_PATH = LOCAL_DIR_PATH / 'Exit.vi'
BUILD_VI_PATH = LOCAL_DIR_PATH / 'Build.vi'


HKLM_KEY = {}
HKLM_KEY[32] = r'SOFTWARE\National Instruments\LabVIEW'
if platform.architecture()[0] == '64bit':
    HKLM_KEY[64], HKLM_KEY[32] = HKLM_KEY[32], r'SOFTWARE\Wow6432Node\National Instruments\LabVIEW'
    
def get_lv_exe_paths(hklm_key):
    """ Detects installed LV instances, accepts single registry key"""
    lv_instances = {}
    for k in HKLM.get_subkey(hklm_key).subkeys():
        # we recognize LV instance by possessing ProductName value
        lv_detected = 'ProductName' in k
        if lv_detected:
            lvpath = Path(k['Path'].data) / 'LabVIEW.exe'
            lv_instances[k['Version'].data] = lvpath

    return lv_instances

def get_lv_exe_path(version=None, bits=32):
    """Finds path and version of installed LV instance.
    
    Examples queries:
    >>> get_lv_exe_path(2015, 32)
    >>> get_lv_exe_path(2015, 64)
    >>> get_lv_exe_path()
    >>> get_lv_exe_path(2015)
    >>> get_lv_exe_path('', 64)
    >>> get_lv_exe_path(15, 64)
    >>> get_lv_exe_path('15.0', 64)
    >>> get_lv_exe_path('15.0.1', 64)
    """
    if version == None:
        version = ''
    if isinstance(version, int):
        version = str(version%2000)
    
    lv_instances = get_lv_exe_paths(HKLM_KEY[bits])

    for ver in lv_instances:
        if ver.startswith(version):
            return lv_instances[ver], ver
    
    return None, None

def exit_labview(time_to_kill=5000):
    """Tries to close running instances of LabVIEW. If cannot be closed gently within time_to_kill milliseconds, LV will be killed
    """
    proc_list = filter(lambda p: p.name()=='LabVIEW.exe', psutil.process_iter())
    @retry(stop_max_delay=time_to_kill)
    def is_closed(proc):
        assert(proc.is_running() == False)

    for p in proc_list:
        lv_exe_path = p.cmdline()[0]
        Popen([lv_exe_path, EXIT_VI_PATH]) #asynchronous
        try:
            is_closed(p)
        except:
            p.kill()
    
def build(lv_exe_path, timeout, tasks):
    """tasks - list of tuples: (projpath, target, buildspec, log_suffix)
    """
    tasks_abs = [ (Path(task[0]).abspath(),
                   task[2],
                   task[1],
                   Path(task[0]).abspath().parent / '{}.{}.{}.log'.format(*task[1:]))
                   for task in tasks ]
    proc = Popen([lv_exe_path, BUILD_VI_PATH, '--'] + [s for t in tasks_abs for s in t])
    try:
        proc.wait(timeout)
    except:
        pass
    finally:
        proc.kill()
    
class LvProj:
    def __init__(self, projpath):
        self.projpath = projpath
        
    def __enter__(self):
        lvproj = open(self.projpath).read().splitlines()
        xml = '\n'.join(lvproj[1:]) # we need to skip header
        self.xmld = Filterable(xmltodict.parse(xml))
        return self
        
    def __exit__(self, type, value, tb):
        with open(self.projpath, 'w') as fh:
            xmltodict.unparse(self.xmld.items[0], pretty=True, output=fh) # header will be added automatically        
    
    def update_symbols(self, symbols, clear_all=False):
        """symbols - dictionary, key:value adds/updates symbol, key:None removes symbol
           clear_all = True - unmentioned symbols are removed from the project
        """
        props = self.xmld['Project']['Property']    
        try:
            ccs = props['CCSymbols']
        except:
            # CCSymbols not found, so add
            ccs = OrderedDict([('@Name', 'CCSymbols'), ('@Type', 'Str'), ('#text', '')])
            props.append(ccs)

        if '#text' not in ccs or clear_all:
            symbols_all = {}
        else:
            symbols_all = OrderedDict((p.split(',') for p in ccs['#text'].split(';') if p))
            
        symbols_all.update(symbols)

        text = ''.join([str(key)+','+str(symbols_all[key])+';' for key in symbols_all if symbols_all[key]])
        ccs['#text'] = text

    def get_lv_version(self):
        """Reads version of LabVIEW which has been used for creating the project.
        """
        full_ver = self.xmld['Project']['@LVVersion']
        return int(full_ver[:2])
        
    def set_app_version(self, target, build_spec, version):
        """Sets version number for given target and build_spec. version - tuple: (major, minor, patch)
        """
        bs = self.xmld['Project']['Item', '@Name', target]['Item', '@Name', 'Build Specifications']['Item', '@Name', build_spec]
        parts = [bs['Property', '@Name', 'Bld_version.' + name] for name in ['major', 'minor', 'patch']]
        for p,v in zip(parts, version):
            p['#text'] = str(v)
        
