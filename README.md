# Python-Synthese-de-Textures

Un projet centré sur la création d'un algorithme qui permet de donner à une image existante
une certaine texture choisie.

Exemple d'utilisation:


## Synthèse de texture
from synthese import quilt_cut, texture_transfer
import imageio.v2 as imageio

texture = imageio.imread("brick.jpg")
image = imageio.imread("face.jpg")

result = quilt_cut(texture, (512, 512), patchsize=40, overlap=10)

## Transfert de texture
from synthese import quilt_cut, texture_transfer
import imageio.v2 as imageio

texture = imageio.imread("brick.jpg")
image = imageio.imread("face.jpg")

result = texture_transfer(texture, image, patchsize=40, overlap=10, tol=0.1)
