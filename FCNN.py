import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import math
from collections import defaultdict

class search_expanded_loss(nn.Module):
    def __init__(self, branching_factor = 3):
        super(search_expanded_loss, self).__init__()
        self.bf = branching_factor

    def forward(self, target, output):
        distance_from_goal = target[:, 0]
        weight = 1 / self.bf ** (distance_from_goal)
        return torch.mean(weight * (target[:, 0] - output[:, 0]) ** 2)

class balanced_data_loss(nn.Module):
    def __init__(self):
        super(balanced_data_loss, self).__init__()

    def get_weights(self, values):
        rounded_values = torch.round(values[:, 0])
        _, inverses, counts = torch.unique(rounded_values, \
                return_counts = True, return_inverse = True)
        return counts[inverses[range(rounded_values.shape[0])]]

    def forward(self, target, output):
        w = self.get_weights(target)
        max_w = torch.max(w)
        #print(max_w.item() / w.float())
        #print(max_w.item() / w)
        return torch.mean((max_w.item() / w.float()) * ((target[:, 0] - output[:, 0]) ** 2))

class discor_loss(nn.Module):

    def __init__(self, update_freq):
        super(discor_loss, self).__init__()
        self.delta = defaultdict(int)
        self.gamma = 1
        self.tau = 10
        self.update_freq = update_freq
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    def forward(self, target, output, input):

        input = input.cpu()
        with torch.no_grad():
            diff = torch.abs(target[:, 0] - output[:, 0])
        weights = torch.zeros((len(input)), device = self.device)

        for i in range(len(input)):
            input_tup = tuple(input[i].numpy())
            weights[i] = math.exp(-self.gamma * self.delta[input_tup] / self.tau)

        delta_mean = 0
        for i in range(len(input)):
            input_tup = tuple(input[i].numpy())
            self.delta[input_tup] = diff[i] + self.gamma * self.delta[input_tup]
            delta_mean += self.delta[input_tup]

        delta_mean = delta_mean / len(input)
        self.tau = (1 - self.update_freq) * self.tau + self.update_freq * delta_mean
        print(weights[:15])
        #return torch.mean(weights * (target[:, 0] - output[:, 0]) ** 2)
        return torch.mean(weights * (target[:, 0] - output[:, 0]) ** 2)

class discor_nn_loss(nn.Module):

    def __init__(self, nn, update_freq = 0.01):
        super(discor_nn_loss, self).__init__()
        self.delta = nn # make delta neural network
        delta = nn # make delta neural network
        self.gamma = 1
        self.tau = 10
        self.update_freq = update_freq
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

    def forward(self, target, output, input):

        #return torch.mean((target[:, 0] - output[:, 0]) ** 2)
        with torch.no_grad():
            diff = torch.abs(target[:, 0] - output[:, 0]).unsqueeze(1)
            deltas = self.delta.predict(input)
            weights = torch.exp(-self.gamma * deltas / self.tau)

            delta_target = diff + self.gamma * deltas

        delta_mean = 0

        self.delta.run_epoch(input, delta_target)

        delta_mean = torch.mean(self.delta.predict(input)) # want to approximate as original mean for speed up?

        self.tau = (1 - self.update_freq) * self.tau + self.update_freq * delta_mean
        print("weights", weights[:15], weights.min(), weights.max())
        #return torch.mean(weights * (target[:, 0] - output[:, 0]) ** 2)
        return torch.mean((target[:, 0] - output[:, 0]) ** 2)

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
