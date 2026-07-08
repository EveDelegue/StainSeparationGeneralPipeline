from pathlib import Path
from torch.utils.data import Dataset
from torchvision.io import decode_image, ImageReadMode
from torchvision.transforms import v2

import torch


class StainSet(Dataset):

    def __init__(self, data_path:str, transforms=v2.Compose([v2.Resize((256,256))])):
        self.data_path = Path(data_path)
        self.files = sorted(self.data_path.glob("*.png")) +sorted(self.data_path.glob("*.jpg")) 
        self.transforms = transforms

    def __getitem__(self, idx):
        img_path = self.files[idx]
        img = decode_image(img_path,mode=ImageReadMode(3)) # read image in RGB
        img = self.transforms(img)
        V = -torch.log(torch.clamp(img,1)/255)
        V = V.reshape(3,-1)
        return V,img
    
    def __len__(self):
        return len(self.files)