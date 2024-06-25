from ToMoDL.models.models_system import MoDLReconstructor
import matplotlib.pyplot as plt
from pathlib import Path
import ToMoDL.utilities.dataloading_utilities as dlutils
from config import model_system_dict, trainer_system_dict, dataloader_system_dict
from torch.utils.data import DataLoader
import torch
import socket
from torch_radon24 import Radon as thrad
import pdb

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(device)

# Load model
# DP win
if socket.gethostname() == 'DESKTOP-SLRK827':
    artifact_tomodl_dir = 'C://Users/David Palecek/Documents/Python_projects/tomodl/ToMoDL/datasets/x20/140114_5dpf_body_20/'
# DP ubuntu qbi1
elif socket.gethostname() == 'qbi1':
    artifact_tomodl_dir = '/home/davidp/python_repos/tomodl/ToMoDL/datasets/x20/140114_5dpf_body_20'
model_tomodl = MoDLReconstructor.load_from_checkpoint(Path(artifact_tomodl_dir) / "model.ckpt", kw_dictionary_model_system = model_system_dict)

# Load dataset
dataset_dict = {
    # 'root_folder' : 'C://Users/David Palecek/Documents/Python_projects/tomodl/ToMoDL/datasets/x20/140114_5dpf_body_20', # In our case, datasets/x20/140114_5dpf_body_20
    'root_folder' : '/home/davidp/python_repos/tomodl/ToMoDL/datasets/x20/140114_5dpf_body_20',
    'acceleration_factor' : 20,
    'transform' : None}

test_dataset = dlutils.ReconstructionDataset(**dataset_dict)
test_dataloader = DataLoader(test_dataset, 
                            batch_size = 1,
                            shuffle = False,
                            num_workers = 0)

# Extract image from dataloader and move it to CPU after processing
us_unfil_im, us_fil_im, fs_fil_im = next(iter(test_dataloader)) # Unfiltered undersampled and filtered undersampled and fully sampled FBP
unfil_im = us_unfil_im.numpy().squeeze()
fil_im = us_fil_im.numpy().squeeze()
fs_im = fs_fil_im.numpy().squeeze()

print(us_unfil_im.shape, us_unfil_im.to(device).shape)

## testing the radon transform
radon = thrad(image_size=us_unfil_im.shape[-1],
              n_angles=720, circle=True,
              det_count=None, device=device)
sinogram = radon(us_unfil_im.to(device))
print(sinogram.shape)

backproj = radon.filter_backprojection(sinogram)
print(backproj.shape)

plt.figure()
plt.subplot(131)
plt.imshow(sinogram[0,0,...].cpu().numpy())
plt.subplot(132)
plt.imshow(backproj[0,0,...].cpu().numpy())
plt.subplot(133)
plt.imshow(us_unfil_im[0,0,...].cpu().numpy())
plt.show()
# pdb.set_trace()
image_tomodl = model_tomodl(us_unfil_im.to(device))['dc'+str(model_tomodl.model.K)][0,0,...].detach().cpu().numpy() # Model Output

# Plot comparison
plt.figure(figsize=(15, 3))
plt.subplot(141)
plt.imshow(unfil_im)
plt.colorbar()
plt.title('Unfileterd')

plt.subplot(142)
plt.imshow(fil_im)
plt.colorbar()
plt.title('Filtered')

plt.subplot(143)
plt.imshow(fs_im)
plt.colorbar()
plt.title('Full image')

plt.subplot(144)
plt.imshow(image_tomodl)
plt.colorbar()
plt.title('inference')

plt.tight_layout()
plt.show()
