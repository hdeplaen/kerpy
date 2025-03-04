import kerch
import torch
from matplotlib import pyplot as plt

num_input, dim_input = 20, 5
sample = torch.randn(num_input, dim_input)

k1 = kerch.kernel.Exponential(sample=sample, sigma=3)
k2 = kerch.kernel.Exponential(sample=sample, distance='chebyshev', sigma=3)

fig, axs = plt.subplots(1,2)
axs[0].imshow(k1.K)
axs[0].set_title("Exponential (Euclidean)")
im = axs[1].imshow(k2.K)
axs[1].set_title("Exponential (Chebyshev)")
fig.colorbar(im, ax=axs.ravel().tolist(), orientation='horizontal')

for ax in axs.flat:
    ax.set_xticks([])
    ax.set_yticks([])