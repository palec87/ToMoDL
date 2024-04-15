'''
K-Folding script
author: obanmarcos
'''
import os
import os, sys
from config import * 

sys.path.append(where_am_i())

import pytorch_lightning as pl
import argparse
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from utilities import dataloading_utilities as dlutils
from utilities.folders import *

from training import train_utilities as trutils

from models.models_system import MoDLReconstructor
import torch


from pytorch_lightning.callbacks import ModelCheckpoint
from pytorch_lightning.loggers import WandbLogger

from torchvision import transforms as T
from pytorch_msssim import SSIM
# from torchmetrics import StructuralSimilarityIndexMeasure as SSIM
from torchmetrics.image import MultiScaleStructuralSimilarityIndexMeasure as MSSSIM

# Options for folding menu
use_default_model_dict = True
use_default_dataloader_dict = True
use_default_trainer_dict = True

profiler = None

def runs(testing_options):
# Model dictionary
    if use_default_model_dict == True:
        #U-Net model
        unet_dict = {'n_channels': 1,
                     'n_classes':1,
                     'bilinear': True,
                     'batch_norm': True,
                     'batch_norm_inconv':True,
                     'residual':True,
                     'up_conv': False}

        # Training parameters
        loss_dict = {'loss_name': 'psnr',
                    'psnr_loss': torch.nn.MSELoss(reduction = 'mean'),
                    'ssim_loss': SSIM(data_range=1, size_average=True, channel=1),
                    'msssim_loss': MSSSIM(kernel_size = 1)}

        # Optimizer parameters
        optimizer_dict = {'optimizer_name': 'Adam+Tanh',
                        'lr': 1e-4}

        # System parameters
        model_system_dict = {'optimizer_dict': optimizer_dict,
                            'method':'unet',
                            'kw_dictionary_unet': unet_dict,
                            'loss_dict': loss_dict,                        
                            'track_train': True,
                            'track_val': True,
                            'track_test': True,
                            'save_model': True,  # this was a bug, throwing an error in the TrainerSystem class, process_kwdictionary in models_system.py
                            'save_path': model_folder,  # same as above
                            'load_model': False,  # same as above
                            }
    
    # PL Trainer and W&B logger dictionaries
    if use_default_trainer_dict == True:
                
        logger_dict = {'project':'deepopt',
                        'entity': 'dpalec', 
                        'log_model': True}

        lightning_trainer_dict = {'max_epochs': 2,  # orig value 40
                                  'log_every_n_steps': 2,  # orig value 10
                                  'check_val_every_n_epoch': 1,
                                  'gradient_clip_val' : 0.5,
                                  'accelerator' : 'gpu', 
                                  'devices' : 1,
                                  'fast_dev_run' : False,
                                  'default_root_dir': model_folder}

        trainer_dict = {'lightning_trainer_dict': lightning_trainer_dict,
                        'use_k_folding': False, 
                        'track_checkpoints': True,
                        'epoch_number_checkpoint': 5,  # orig value 10
                        'use_swa' : False,
                        'use_accumulate_batches': False,
                        'k_fold_number_datasets': 1,
                        'use_logger' : True,
                        'resume':'allow',
                        'logger_dict': logger_dict,
                        'track_default_checkpoints'  : False,
                        'use_auto_lr_find': False,
                        'batch_accumulate_number': 3,
                        'use_mixed_precision': False,
                        'batch_accumulation_start_epoch': 0, 
                        'profiler': profiler,
                        'restore_fold': False,
                        'fold_number_restore': 1,
                        'acc_factor_restore': 22}

    # Dataloader dictionary
    if use_default_dataloader_dict == True:
        
        # data_transform = T.Compose([T.ToTensor()])
        data_transform = None                                    
        
        dataloader_dict = {'datasets_folder': datasets_folder,
                           'number_volumes' : 0,
                           'experiment_name': 'Bassi',
                           'img_resize': 100,
                           'load_shifts': True,
                           'save_shifts':False,
                           'number_projections_total': 720,
                           'number_projections_undersampled': 720//20,
                           'acceleration_factor':20,
                           'train_factor' : 0.8, 
                           'val_factor' : 0.2,
                           'test_factor' : 0.2, 
                           'batch_size' : 8, 
                           'sampling_method' : 'equispaced-linear',
                           'shuffle_data' : True,
                           'data_transform' : data_transform,
                           'num_workers' : 2,  # original value 8
                           'use_subset_by_part': False}  # this was a bug
    
    if 'cpu' in testing_options:
        lightning_trainer_dict['accelerator'] = 'cpu'
        
    # Create Custom trainer
    if 'train_ssim' in testing_options:

        with torch.autograd.set_detect_anomaly(True):

            model_system_dict['loss_dict']['loss_name'] = 'ssim'

            trainer = trutils.TrainerSystem(trainer_dict, dataloader_dict, model_system_dict)
            trainer.k_folding()

    if 'train_psnr' in testing_options:
        
        model_system_dict['loss_dict']['loss_name'] = 'psnr'

        trainer = trutils.TrainerSystem(trainer_dict, dataloader_dict, model_system_dict)
        trainer.train_model()
        # trainer.k_folding()


if __name__ == '__main__':

    train_options = []

    parser = argparse.ArgumentParser(description='Do K-folding with different networks')

    parser.add_argument('--train_psnr', help = 'Train w/PSNR loss with optimal hyperparameters', action="store_true")
    parser.add_argument('--train_ssim', help = 'Train w/SSIM loss with optimal hyperparameters', action="store_true")
    parser.add_argument('--cpu', help = 'Use CPU', action="store_true")
    
    args = parser.parse_args()

    if args.train_psnr:

        print('Training UNET with PSNR loss...')
        train_options.append('train_psnr')
    
    if args.train_ssim:
        
        print('Training UNET with SSIM loss...')
        train_options.append('train_ssim')
    
    if args.cpu:

        print('Training on CPU')
        train_options.append('cpu')

    runs(train_options)