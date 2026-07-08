import hydra
from omegaconf import DictConfig
from utils.StainSet import StainSet
from utils.utils import reconstruct_store_imgs
from torch.utils.data import DataLoader
import models.PGA as pga
import torch

@hydra.main(version_base=None, config_path="conf", config_name="config")

def main(cfg : DictConfig) -> None:
    device = "cuda" if torch.cuda.is_available() else "cpu"
    # load data
    data_path = cfg.paths.dataset_0
    dataset = StainSet(data_path,)
    dataloader = DataLoader(dataset,batch_size=cfg.loader.batch_size,shuffle=False)
    # init PGA
    W0 = torch.tensor(cfg.colors.W0)
    pga_model = pga.PGA(W0,device)

    # apply it
    for V,img in dataloader:
        H = pga_model(V)
        # store intermediate images
        reconstruct_store_imgs(W0,H,"visuals","full",img.shape[2],img.shape[3])




    

if __name__ == "__main__":
    main()