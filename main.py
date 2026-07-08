import hydra
from omegaconf import DictConfig
from utils.StainSet import StainSet
from utils.utils import reconstruct_store_imgs
from torch.utils.data import DataLoader
import models.PGA as pga
import torch
import tqdm
import os

@hydra.main(version_base=None, config_path="conf", config_name="config")

def main(cfg : DictConfig) -> None:
    device = "cuda" if torch.cuda.is_available() else "cpu"
    # load data
    data_path = cfg.paths.dataset
    dataset = StainSet(data_path)
    dataloader = DataLoader(dataset,batch_size=1,shuffle=False)
    # init dummy PGA
    W0 = torch.tensor(cfg.colors.W0)
    dummy_pga_model = pga.dummy_PGA(W0,device)

    # apply it
    with torch.no_grad():
        for i,(V,img) in tqdm.tqdm(enumerate(dataloader)):
            H = dummy_pga_model(V)
            # store intermediate images
            reconstruct_store_imgs(W0,H,cfg.verbose ,os.path.join(cfg.paths.verbose,f"img_{i}"),"full",img.shape[2],img.shape[3])




    

if __name__ == "__main__":
    main()