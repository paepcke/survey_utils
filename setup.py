import subprocess
import sys


known_modules = ['table_utils', 'math_utils', 'plotting_utils']

def setup_module(cmd, module):
    if module == 'table_utils':
        subprocess.call(['python', 'setup_table_utils.py', cmd])
    elif module == 'math_utils':
        subprocess.call(['python', 'setup_math_utils.py', cmd])
    elif module == 'plotting_utils':
        subprocess.call(['python', 'setup_plotting_utils.py', cmd])
    else:
        raise ValueError("Module '%s' unknown." % module)        

if __name__ == '__main__':
    
    usage = 'python setup.py <setup-command> { table_utils | math_utils | plotting_utils}*'
    if len(sys.argv) < 2:
        print(usage)
        sys.exit()
        
    cmd = sys.argv[1]
    modules_to_process = sys.argv[2:]
    if len(modules_to_process) == 0:
        # Process all:
        modules_to_process = known_modules
    
    for mod_to_process in modules_to_process:
        print("*****Processing %s for module %s..." % (cmd, mod_to_process))
        setup_module(cmd, mod_to_process)
        