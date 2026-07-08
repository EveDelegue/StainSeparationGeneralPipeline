import torch
import matplotlib.pyplot as plt
import os

def gen_HE_image(W, H, N:int=500, M:int=500):
    BS = len(H)
    W0 = -torch.log(W/255)
    chanel_OD = W0[:,0:2] @ H[:,0:2,:]
    chanel_img = torch.exp(-chanel_OD.reshape(BS, 3, N, M))

    return chanel_img

def gen_image(W, H, N:int=500, M:int=500):
    BS = len(H)
    W0 = -torch.log(W/255)
    chanel_OD = W0 @ H
    chanel_img = torch.exp(-chanel_OD.reshape(BS, 3, N, M))

    return chanel_img

def gen_chanels(W, H, N:int=500, M:int=500):
    W0 = -torch.log(W/255)
    BS = len(H)
    imgs_list = []
    for chanel in range(W0.shape[1]):
        chanel_OD = W0[:,chanel:chanel+1] @ H[:,chanel:chanel+1,:]
        chanel_img = torch.exp(-chanel_OD.reshape(BS, 3, N, M))
        imgs_list.append(chanel_img)
    return imgs_list

def reconstruct_store_imgs(W,H,verbose:bool=False,visuals_dir:str="visuals",shown:str="full",N:int=256,M:int=256):

    os.makedirs(visuals_dir, exist_ok=True)

    img = gen_image(W,H,N,M)
    if verbose:
            plt.imsave( os.path.join(visuals_dir , f"sample_{shown}.png"),img.squeeze().cpu().permute(1,2,0))
    img_HE = gen_HE_image(W,H,N,M)
    plt.imsave( os.path.join(visuals_dir , f"sample_HE.png"),img_HE.squeeze().cpu().permute(1,2,0))
    
    imgs_list = gen_chanels(W,H,N,M)
    if verbose:
        for id,chanel in enumerate(imgs_list):
                plt.imsave( os.path.join(visuals_dir , f"sample_{id}.png"),chanel.squeeze().cpu().permute(1,2,0))
