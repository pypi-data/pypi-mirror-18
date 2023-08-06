import lvappbuilder as ab
import lvappbuilder.sh as sh

def build(proj_path, target, build_spec, version, symbols, repl_in_file, lv_bits, log_suffix, build_timeout):
    """Example of build action. It can be used directly as it is, or just as a template for another action.
    """
    modif_files = {f[0] for f in repl_in_file}
    
    print('Exiting LabVIEW (if running)...')
    ab.exit_labview()
    
    print('Creating backups...')
    for fp in modif_files:
        sh.backup(fp)
    try:
        with ab.LvProj(proj_path) as lvp:
            lv_ver_proj = lvp.get_lv_version()
            print('Updating symbols...')
            lvp.update_symbols(symbols)
            print('Setting app version to', '.'.join(version)+'...')
            lvp.set_app_version(target, build_spec, version)
            
        print('Replacing patterns in files...')
        for rep in repl_in_file:
            sh.replace_in_file(*rep)
            
        print('LabVIEW version detected in project:', lv_ver_proj)
        lv_exe_path, lv_ver = ab.get_lv_exe_path(version=lv_ver_proj, bits=lv_bits)
        print('LabVIEW to be used: {} {}bits: {}'.format(lv_ver, lv_bits, lv_exe_path))

        print('Building...')
        ab.build(lv_exe_path, build_timeout, [(proj_path, target, build_spec, log_suffix)])
    finally:
        print('Restoring original files from backups...')
        for fp in modif_files:
            sh.restore(fp)
        print('Done.')
        print()
