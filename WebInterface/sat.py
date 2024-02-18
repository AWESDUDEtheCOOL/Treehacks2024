from torchvision import models, transforms
import torch
import torch.nn as nn
from torch.nn import functional as F
from PIL import Image
import numpy as np

# https://www.kaggle.com/code/pmigdal/transfer-learning-with-resnet-50-in-pytorch
data_transforms = {
    "train": transforms.Compose(
        [
            transforms.Resize((224, 224)),
            transforms.RandomAffine(0, shear=10, scale=(0.8, 1.2)),
            transforms.RandomHorizontalFlip(),
            transforms.ToTensor(),
        ]
    ),
    "validation": transforms.Compose(
        [
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
        ]
    ),
}

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

model = models.resnet50(pretrained=False).to(device)
model.fc = nn.Sequential(
    nn.Linear(2048, 128),
    nn.ReLU(inplace=True),
    nn.Linear(128, 64),
    nn.ReLU(inplace=True),
    nn.Linear(64, 2),
).to(device)
model.load_state_dict(torch.load("models/weights.h5"))


def make_inference(filepath):
    img_list = [Image.open(img_path) for img_path in [filepath]]

    validation_batch = torch.stack(
        [data_transforms["validation"](img).to(device) for img in img_list]
    )

    pred_logits_tensor = model(validation_batch)
    pred_probs = F.softmax(pred_logits_tensor, dim=1).cpu().data.numpy()
    return 100 * pred_probs[0, 0]
