import sys
import torch # numpy
from torch.autograd import Variable # tensor with gradient
import torch.nn as nn # all layers classes
import torch.nn.functional as F # other functions for building model


class Net(nn.Module): # nn.Module里面到底有什么？

    def __init__(self):
        super(Net, self).__init__() # Module init 到底做了什么？
		
        self.conv1 = nn.Conv2d(1, 6, 5)
        self.conv2 = nn.Conv2d(6, 16, 5)
        # an affine operation: y = Wx + b
        self.fc1 = nn.Linear(16 * 5 * 5, 120) # nn.Linear 在构建什么？
        self.fc2 = nn.Linear(120, 84)
        self.fc3 = nn.Linear(84, 10)

    def forward(self, x):

        x = F.max_pool2d(F.relu(self.conv1(x)), (2, 2)) # 看看F.relu的代码逻辑
        x = F.max_pool2d(F.relu(self.conv2(x)), 2) # 看看F.max_pool2d代码逻辑
        x = x.view(-1, self.num_flat_features(x)) # 在Net.forward里面调用Net.num_flat_features
        x = F.relu(self.fc1(x))# 如何使用Net.forward 和 Net.num_flat_features
        x = F.relu(self.fc2(x))
        x = self.fc3(x)
        return x

    def num_flat_features(self, x): #
        size = x.size()[1:]
        num_features = 1
        for s in size:
            num_features *= s
        return num_features

net = Net()

single_sample = torch.randn(32,32).unsqueeze(0).unsqueeze(0)
inputs = Variable(torch.randn(1, 1, 32, 32))
output = net(inputs)

conv1_weight_1 = list(net.parameters())[0][0]
target = Variable(torch.arange(1, 11))

criterion = nn.MSELoss()
loss = criterion(output, target)

net.zero_grad()     # zeroes the gradient buffers of all parameters
net.conv1.weight.grad

import torch.optim as optim
optimizer = optim.SGD(net.parameters(), lr=0.01)
optimizer.zero_grad() # optimizer.zero_grad() == net.zero_grad()


loss.backward() # 参数的导数，从无到有
optimizer.step() # 只是更新参数，不输出任何值
net.conv1.bias # 展示某层的参数
net.conv1.weight.grad # 展示某层的导数
net.conv1.zero_grad() # 将某层的导数归0
