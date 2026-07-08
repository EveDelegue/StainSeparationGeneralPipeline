import torch

# H only pga 

# le PGA que j'ai trouvé dans un autre projet d'Aymen
## on observe que W n'évolue pas ici, on fait donc la très lourde hypothèse que les couleurs inititiales sont les bonnes
class PGA(torch.nn.Module):
    def __init__(self, Wgt, device, nitm:int=1500, prec:float=1e-4):
        super(PGA, self).__init__()
        self.device = torch.device(device)
        self.W = -torch.log(Wgt.to(device)/255)
        self.max_iters = nitm
        self.tol = prec
    
    def forward(self, V, Lambda:float=1.15e-1):
        # init H
        H = (torch.linalg.pinv(self.W) @ V)
        H = torch.maximum(H, torch.zeros_like(H))
        step_size = 1.995 / (torch.norm(self.W) ** 2 + Lambda)
        for nit in range(self.max_iters):
            Hold = H.clone()
            H_grad = self.W.t() @ (self.W @ H - V) + Lambda * H
            H = (H - step_size * H_grad).clamp_(min=1e-8)
            if nit > 0 and torch.norm(H - Hold) < torch.norm(Hold) * self.tol:
                break
        return H

class dummy_PGA(torch.nn.Module):
    def __init__(self, Wgt, device, nitm:int=1500, prec:float=1e-4):
        super(dummy_PGA, self).__init__()
        self.device = torch.device(device)
        self.W = -torch.log(Wgt.to(device)/255)
        self.max_iters = nitm
        self.tol = prec
    
    def forward(self, V, Lambda:float=0.):
        # init H
        H = (torch.linalg.pinv(self.W) @ V)
        H = torch.maximum(H, torch.zeros_like(H))
        return H