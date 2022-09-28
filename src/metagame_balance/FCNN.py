import math
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim


class FCNN(nn.Module):
    def __init__(self, layers, use_batch_norm=True):
        super(FCNN, self).__init__()
        self.device = None
        self.fc = nn.ModuleList()
        for i in range(len(layers) - 1):
            self.fc.append(nn.Linear(layers[i], layers[i+1], bias=True))
        if use_batch_norm:
            self.bns = nn.ModuleList()
            for i in range(len(layers) - 1):
                self.bns.append(nn.BatchNorm1d(layers[i+1]))
        else:
            self.bns = None
        self.params = nn.ModuleList()
        self.params.append(self.fc)

    def forward(self, x):
        for i in range(len(self.fc) - 1):
            #x = F.tanh(self.bns[i](self.fc[i](x)))
            x = F.relu(self.fc[i](x)) if self.bns is None else F.relu(self.bns[i](self.fc[i](x)))
        x = self.fc[-1](x)
        return x

    def save(self, model_path):
        torch.save(self.params.state_dict(), model_path)

    def load_model(self, model_path):
        self.params.load_state_dict(torch.load(model_path))

    def compile(self, loss = nn.MSELoss(), optimizer = optim.Adam, lr=1e-3, loss_input = False):

        self.optimizer = optimizer(self.parameters(), lr = lr)
        self.loss_fn = loss
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.loss_input = loss_input
        self.loss_fn.to(self.device)
        self.to(self.device)

    def predict(self, x, batch_size = 2e4):
        batch_size = int(min(x.shape[0], batch_size))
        n_batches = math.ceil(x.shape[0] / batch_size)
        y = []
        with torch.no_grad():
            self.eval()

            if not torch.is_tensor(x):
                x = torch.Tensor(x)
            for i in range(n_batches):
                local_x = x[i * batch_size:(i+1)*batch_size,].to(self.device)
                y.append(self.forward(local_x))
        return torch.cat(y).squeeze(1).cpu().detach().numpy()

    def run_epoch(self, x, y, batch_size = 1e10, verbose = 1):

        if self.device is None:
            Exception("Make sure you compile the model first!")

        self.train()
        batch_size = min(x.shape[0], batch_size)
        n_batches = math.ceil(x.shape[0] / batch_size)
        running_loss = 0.
        if not torch.is_tensor(x):
            x = torch.Tensor(x)
            y = torch.unsqueeze(torch.Tensor(y), 1)
        for i in range(n_batches):
            local_x, local_y = x[i*batch_size:(i+1)*batch_size,], \
                    y[i*batch_size:(i+1)*batch_size,]

            local_x, local_y = local_x.to(self.device), local_y.to(self.device)

            sample_size = local_x.shape[0]

            self.optimizer.zero_grad()
            pred = self.forward(local_x)
            if self.loss_input:
                loss = self.loss_fn.forward(local_y, pred, local_x)
            else:
                loss = self.loss_fn.forward(local_y, pred)
            loss.backward()

            self.optimizer.step()
            running_loss += loss.item() * sample_size
        running_loss /= x.shape[0]
        if verbose == 1:
            print("Samples used: {} Epoch Loss:{}".format(x.shape[0], running_loss))
        return running_loss

    def run_epoch_weighted(self, x, y, weights, batch_size = 1e10, verbose = 1):

        if self.device is None:
            Exception("Make sure you compile the model first!")

        self.train()
        batch_size = min(x.shape[0], batch_size)
        n_batches = math.ceil(x.shape[0] / batch_size)
        running_loss = 0.
        if not torch.is_tensor(x):
            x = torch.Tensor(x)
            y = torch.unsqueeze(torch.Tensor(y), 1)
        for i in range(n_batches):
            local_x, local_y, local_weight = x[i*batch_size:(i+1)*batch_size,], \
                    y[i*batch_size:(i+1)*batch_size,], weights[i*batch_size:(i+1)*batch_size,]

            local_x, local_y, local_weight = local_x.to(self.device), local_y.to(self.device), local_weight.to(self.device)

            sample_size = local_x.shape[0]

            self.optimizer.zero_grad()
            pred = self.forward(local_x)
            loss = self.loss_fn.forward(local_y, pred, local_weight)
            loss.backward()

            self.optimizer.step()
            running_loss += loss.item() * sample_size
        running_loss /= x.shape[0]
        if verbose == 1:
            print("Samples used: {} Epoch Loss:{}".format(x.shape[0], running_loss))
        return running_loss

    def set_weights(self, weights):
        self.params.load_state_dict(weights)

    def get_weights(self):
        return self.params.state_dict()

    def count_parameters(self):
        return sum(p.numel() for p in self.parameters() if p.requires_grad)
