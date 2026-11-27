import torch
import numpy as np
from PIL import Image

image = Image.open("frame_05.png").convert("L")

array = np.array(image, dtype=np.float32) / 255.0

tensor = torch.from_numpy(array)

tensor = tensor.unsqueeze(0).unsqueeze(0)

tensor = tensor.to("cuda")

print("Размер массива:", array.shape)
print("Размер тензора:", tensor.shape)
print("Устройство:", tensor.device)
print("Минимум:", tensor.min().item())
print("Максимум:", tensor.max().item())

print("DinoVision успешно передал изображение в PyTorch!")