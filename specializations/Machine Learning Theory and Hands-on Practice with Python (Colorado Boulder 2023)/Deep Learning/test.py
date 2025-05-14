import torch
from torch.autograd import grad
from graphviz import Digraph
from torchviz import make_dot
import matplotlib.pylab as plt

def make_dot1(var):
    node_attr = dict(style='filled',
                     shape='box',
                     align='left',
                     fontsize='12',
                     ranksep='0.1',
                     height='0.2')
    dot = Digraph(node_attr=node_attr, graph_attr=dict(size="12,12"))
    seen = set()

    def add_nodes(var):
        if var not in seen:
            if isinstance(var, Variable):
                value = '('+(', ').join(['%d'% v for v in var.size()])+')'
                dot.node(str(id(var)), str(value), fillcolor='lightblue')
            else:
                dot.node(str(id(var)), str(type(var).__name__))
            seen.add(var)
            if hasattr(var, 'previous_functions'):
                for u in var.previous_functions:
                    dot.edge(str(id(u[0])), str(id(var)))
                    add_nodes(u[0])
    add_nodes(var.creator)
    return dot

x = torch.ones(1, 1, requires_grad=True)
v = x + 2
y = v ** 2

grad(outputs=y, inputs=x) #dy_hat_dx

x1 = torch.ones(1, 1)
x2 = -torch.ones(1, 1)
w11 = 0.5*torch.ones(1, 1, requires_grad=True)
w21 = 0.5*torch.ones(1, 1, requires_grad=True)
w12 = torch.zeros(1, 1, requires_grad=True)
w22 = torch.ones(1, 1, requires_grad=True)
w13 = torch.ones(1, 1, requires_grad=True)
w23 = torch.zeros(1, 1, requires_grad=True)
z1 = x1*w11 + x2*w21
z2 = x1*w12 + x2*w22
z3 = x1*w13 + x2*w23
h1 = torch.sigmoid(z1)
h2 = torch.sigmoid(z2)
h3 = torch.sigmoid(z3)
w1 = -torch.ones(1, 1, requires_grad=True)
w2 = 0.5*torch.ones(1, 1, requires_grad=True)
w3 = 0.5*torch.ones(1, 1, requires_grad=True)
z = h1*w1 + h2*w2 + h3*w3
a = torch.sigmoid(z)
y = torch.ones(1, 1)
L = -y*torch.log(a) - (1-y)*torch.log(1-a)

d = make_dot(L)
d.format = "png"
d.render("attached") 

print('done')
#plt.show()

grad(outputs=L, inputs=w11, retain_graph=True) #dy_hat_dx
grad(outputs=L, inputs=z, retain_graph=True)

import torchvision.models as models
x = torch.zeros(1, 3, 224, 224, dtype=torch.float, requires_grad=False)
resnet = models.resnet50(pretrained=True)
out = resnet(x)
make_dot(out)

