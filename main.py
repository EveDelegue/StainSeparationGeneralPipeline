import hydra
from omegaconf import DictConfig

@hydra.main(version_base=None, config_path="conf", config_name="config")

def main(cfg : DictConfig) -> None:
    data_path = cfg.paths.dataset_0
    

if __name__ == "__main__":
    main()