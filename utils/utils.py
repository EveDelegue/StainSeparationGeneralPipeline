import torch
import matplotlib.pyplot as plt
import os

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

def reconstruct_store_imgs(W,H,visuals_dir,shown,N,M):

    os.makedirs(visuals_dir, exist_ok=True)

    imgs_list = gen_image(W,H,N,M)
    for i,img in enumerate(imgs_list):
        save_dir = os.path.join(visuals_dir,  f"pred_{i}")
        os.makedirs(save_dir,exist_ok=True)
        plt.imsave( os.path.join(save_dir , f"sample_{shown}_{i}.png"),img.cpu().permute(1,2,0))
    imgs_list = gen_chanels(W,H,N,M)
    for id,chanel_list in enumerate(imgs_list):
        for i,img in enumerate(chanel_list):
            save_dir = os.path.join(visuals_dir,  f"pred_{i}")
            plt.imsave( os.path.join(save_dir , f"sample_{id}_{i}.png"),img.cpu().permute(1,2,0))
