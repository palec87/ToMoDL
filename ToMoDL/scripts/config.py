import sys
import socket

marcos_computer_path = '/home/obanmarcos/Balseiro/DeepOPT' 
marcos_computer_path_datasets = '/home/obanmarcos/Balseiro/DeepOPT/datasets/'
marcos_computer_path_metrics = '/home/obanmarcos/Balseiro/DeepOPT/metrics/' 
marcos_computer_path_models = '/home/obanmarcos/Balseiro/DeepOPT/models/' 
german_computer_path = '/home/marcos/DeepOPT/'
german_computer_path_datasets = '/data/marcos/datasets/'
ariel_computer_path = '/home/marcos/DeepOPT'
ariel_computer_path_datasets = '/Datos/DeepOPT'

dp_computer_path = 'C://Users/David Palecek/Documents/Python_projects/tomodl/ToMoDL/ToMoDL/'
dp_computer_path_datasets = 'C://Users/David Palecek/Documents/Python_projects/tomodl/ToMoDL/datasets/'
dp_computer_path_metrics = 'C://Users/David Palecek/Documents/Python_projects/tomodl/ToMoDL/metrics/'
dp_computer_path_models = 'C://Users/David Palecek/Documents/Python_projects/tomodl/ToMoDL/ToMoDL/models/'

def where_am_i(path = None):

    if socket.gethostname() in ['copote', 'copito']:
        if path == 'datasets':
            return marcos_computer_path_datasets
        elif path == 'models':
            return marcos_computer_path_models
        elif path == 'metrics':
            return marcos_computer_path_metrics
        else:
            return marcos_computer_path

    elif socket.gethostname() == 'cabfst42':
        if path == 'datasets':
            return german_computer_path_datasets
        else:
            return german_computer_path
    elif socket.gethostname() == 'gpu1':
        if path == 'datasets':
            return ariel_computer_path_datasets
        else:   
            return ariel_computer_path
    elif socket.gethostname() == 'DESKTOP-SLRK827':
        if path == 'datasets':
            return dp_computer_path_datasets
        elif path == 'models':
            return dp_computer_path_models
        elif path == 'metrics':
            return dp_computer_path_metrics
        else:
            return dp_computer_path
        
    elif socket.gethostname() == 'qbi1':
        if path == 'datasets':
            return '/home/davidp/python_repos/tomodl/ToMoDL/datasets/'
        elif path == 'models':
            return '/home/davidp/python_repos/tomodl/ToMoDL/models/'
        elif path == 'metrics':
            return '/home/davidp/python_repos/tomodl/ToMoDL/metrics/'
        else:
            return '/home/davidp/python_repos/tomodl/ToMoDL/ToMoDL/'
    else:
        print('Computer not found')
        sys.exit(0)

