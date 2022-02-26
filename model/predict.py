import torch.nn as nn
from torchvision import transforms
from torchvision.models import resnet18

def transform(img):
    _transform = transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225]),
    ])
    return _transform(img)

class Net(nn.Module):

    def __init__(self):
        super().__init__()

        self.feature = resnet18(pretrained=True)
        self.fc = nn.Linear(1000, 6)

    def forward(self, x):
        h = self.feature(x)
        h = self.fc(h)
        return h