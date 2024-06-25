"""
Folders to be used in data processing 
author: obanmarcos
"""

import sys
import socket

if socket.gethostname() in ['copote', 'copito']:
    main_folder = '/data/marcos/DataOPT/'
    results_folder = '/home/marcos/DeepOPT/Resultados/'
    model_folder = '/home/marcos/DeepOPT/SavedModels/'
    datasets_folder = '/data/marcos/datasets/'
    volumes_folder = '/home/marcos/DeepOPT/Volumes/'

elif socket.gethostname() == 'DESKTOP-SLRK827':
    main_folder = 'C://Users/David Palecek/Documents/Python_projects/tomodl/ToMoDL/datasets/'
    results_folder = 'C://Users/David Palecek/Documents/Python_projects/tomodl/Results/'
    model_folder = 'C://Users/David Palecek/Documents/Python_projects/tomodl/SavedModels/'
    datasets_folder = 'C://Users/David Palecek/Documents/Python_projects/tomodl/ToMoDL/datasets/'
    volumes_folder = 'C://Users/David Palecek/Documents/Python_projects/tomodl/Volumes/'

elif socket.gethostname() == 'qbi1':
    main_folder = '/home/davidp/python_repos/tomodl/ToMoDL/datasets/'
    results_folder = '/home/davidp/python_repos/tomodl/Results/'
    model_folder = '/home/davidp/python_repos/tomodl/SavedModels/'
    datasets_folder = '/home/davidp/python_repos/tomodl/ToMoDL/datasets/'
    volumes_folder = '/home/davidp/python_repos/tomodl/Volumes/'
else:
    print('Computer not found')
    sys.exit(0)


f140114_5dpf = main_folder+'140114_5dpf'  # 5 days post-fertilization
f140117_3dpf = main_folder+'140117_3dpf'  # 3 days post-fertilization
f140115_1dpf = main_folder+'140315_1dpf'  # 1 days post-fertilization

f140315_3dpf = main_folder+'140315_3dpf'     # 3 days post-fertilization
f140415_5dpf_4X = main_folder+'140415_5dpf_4X'  # 5 days post-fertilization
f140419_5dpf = main_folder+'140519_5dpf'     # 5 days post-fertilization

f140714_5dpf = main_folder+'140714_5dpf'
f140827_3dpf_4X = main_folder+'140827_3dpf_4X'
f140827_5dpf_4X = main_folder+'140827_5dpf_4X'
