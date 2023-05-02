import torch
import torch.nn as nn
from torch.distributions import MultivariateNormal
from torch.distributions import Categorical
import numpy
from model.business_model.checker import Checker
from model.business_model.token_array import TokenArray
import pickle
################################## set device ##################################
print("============================================================================================")
# set device to cpu or cuda
device = torch.device('cpu')
if (torch.cuda.is_available()):
    device = torch.device('cuda:0')
    torch.cuda.empty_cache()
    print("Device set to : " + str(torch.cuda.get_device_name(device)))
else:
    print("Device set to : cpu")
print("============================================================================================")


################################## PPO Policy ##################################
class RolloutBuffer:
    def __init__(self):
        self.actions = []
        self.states = []
        self.logprobs = []
        self.rewards = []
        self.state_values = []
        self.is_terminals = []

    def clear(self):
        del self.actions[:]
        del self.states[:]
        del self.logprobs[:]
        del self.rewards[:]
        del self.state_values[:]
        del self.is_terminals[:]


def get_mask(player_ID):
    player_str = 'player' + str(player_ID)
    # read the pickle
    state = pickle.load(open('obs.pkl', 'rb'))
    mask = numpy.zeros(88)
    shop_cards_rank1 = state['shop']['rank1_cards']
    shop_cards_rank2 = state['shop']['rank2_cards']
    shop_cards_rank3 = state['shop']['rank3_cards']
    # if the shop of rank 1 is empty, padd the shop with none
    if len(shop_cards_rank1) != 4:
        # padd with none shop_cards_rank1 until it has 4 cards
        for i in range(4 - len(state['shop']['rank1_cards'])):
            shop_cards_rank1.append(None)

    # if the shop of rank 2 is empty, padd the shop with none
    if len(shop_cards_rank2) != 4:
        for i in range(4 - len(state['shop']['rank2_cards'])):
            shop_cards_rank2.append(None)
    # if the shop of rank 3 is empty, padd the shop with none
    if len(shop_cards_rank3) != 4:
        for i in range(4 - len(state['shop']['rank3_cards'])):
            shop_cards_rank3.append(None)
    # remove the none from the reserved cards
    number_card_reserved = len(
        [x for x in state[player_str]['reserved'] if x is not None])
    shop_cards = [shop_cards_rank1, shop_cards_rank2, shop_cards_rank3]

    mask = Checker.get_mask(state[player_str]['cards'], shop_cards, state['shop']['rank1_size'], state['shop']['rank2_size'], state['shop']['rank3_size'], number_card_reserved, TokenArray(state[player_str]['tokens']), state['shop']['tokens'], state[player_str]['reserved'],
                            state[player_str]['object'])

    return mask


class ActorCritic(nn.Module):
    def __init__(self, state_dim, action_dim, has_continuous_action_space, action_std_init):
        super(ActorCritic, self).__init__()

        self.has_continuous_action_space = has_continuous_action_space

        if has_continuous_action_space:
            self.action_dim = action_dim
            self.action_var = torch.full(
                (action_dim,), action_std_init * action_std_init).to(device)
        # actor
        if has_continuous_action_space:
            self.actor = nn.Sequential(
                nn.Linear(state_dim, 64),

                nn.Linear(64, action_dim),
                nn.Tanh()
            )
        else:
            self.actor = nn.Sequential(
                nn.Linear(state_dim, 32),
                nn.ReLU(),
                nn.Linear(32, action_dim),
                nn.Softmax(dim=-1)
            )
        # critic
        self.critic = nn.Sequential(
            nn.Linear(state_dim, 32),
            nn.ReLU(),
            nn.Linear(32, 1)
        )

    def set_action_std(self, new_action_std):
        if self.has_continuous_action_space:
            self.action_var = torch.full(
                (self.action_dim,), new_action_std * new_action_std).to(device)
        else:
            print(
                "--------------------------------------------------------------------------------------------")
            print(
                "WARNING : Calling ActorCritic::set_action_std() on discrete action space policy")
            print(
                "--------------------------------------------------------------------------------------------")

    def forward(self):
        raise NotImplementedError

    def act(self, state):

        if self.has_continuous_action_space:
            action_mean = self.actor(state)
            cov_mat = torch.diag(self.action_var).unsqueeze(dim=0)
            dist = MultivariateNormal(action_mean, cov_mat)
        else:
            action_probs = self.actor(state)
            # print('action_probs',action_probs)
            action_probs = action_probs * \
                torch.from_numpy(get_mask(1)).to(device)
            dist = Categorical(action_probs)
            # print('dist',dist.probs)
        action = dist.sample()
        action_logprob = dist.log_prob(action)
        state_val = self.critic(state)

        return action.detach(), action_logprob.detach(), state_val.detach()

    def evaluate(self, state, action):

        if self.has_continuous_action_space:
            action_mean = self.actor(state)

            action_var = self.action_var.expand_as(action_mean)
            cov_mat = torch.diag_embed(action_var).to(device)
            dist = MultivariateNormal(action_mean, cov_mat)

            # For Single Action Environments.
            if self.action_dim == 1:
                action = action.reshape(-1, self.action_dim)
        else:
            action_probs = self.actor(state)
            action_probs = action_probs * \
                torch.from_numpy(get_mask(1)).to(device)

            dist = Categorical(action_probs)

        action_logprobs = dist.log_prob(action)
        dist_entropy = dist.entropy()
        state_values = self.critic(state)

        return action_logprobs, state_values, dist_entropy


class PPO:
    def __init__(self, state_dim, action_dim, lr_actor, lr_critic, gamma, K_epochs, eps_clip,
                 has_continuous_action_space, action_std_init=0.6):

        self.has_continuous_action_space = has_continuous_action_space

        if has_continuous_action_space:
            self.action_std = action_std_init

        self.gamma = gamma
        self.eps_clip = eps_clip
        self.K_epochs = K_epochs

        self.buffer = RolloutBuffer()

        self.policy = ActorCritic(
            state_dim, action_dim, has_continuous_action_space, action_std_init).to(device)
        self.optimizer = torch.optim.Adam([
            {'params': self.policy.actor.parameters(), 'lr': lr_actor},
            {'params': self.policy.critic.parameters(), 'lr': lr_critic}
        ])

        self.policy_old = ActorCritic(
            state_dim, action_dim, has_continuous_action_space, action_std_init).to(device)
        self.policy_old.load_state_dict(self.policy.state_dict())

        self.MseLoss = nn.MSELoss()

    def set_action_std(self, new_action_std):
        if self.has_continuous_action_space:
            self.action_std = new_action_std
            self.policy.set_action_std(new_action_std)
            self.policy_old.set_action_std(new_action_std)
        else:
            print(
                "--------------------------------------------------------------------------------------------")
            print(
                "WARNING : Calling PPO::set_action_std() on discrete action space policy")
            print(
                "--------------------------------------------------------------------------------------------")

    def decay_action_std(self, action_std_decay_rate, min_action_std):
        print("--------------------------------------------------------------------------------------------")
        if self.has_continuous_action_space:
            self.action_std = self.action_std - action_std_decay_rate
            self.action_std = round(self.action_std, 4)
            if (self.action_std <= min_action_std):
                self.action_std = min_action_std
                print(
                    "setting actor output action_std to min_action_std : ", self.action_std)
            else:
                print("setting actor output action_std to : ", self.action_std)
            self.set_action_std(self.action_std)

        else:
            print(
                "WARNING : Calling PPO::decay_action_std() on discrete action space policy")
        print("--------------------------------------------------------------------------------------------")

    def select_dummy_action(self, state):
        with torch.no_grad():
            state = torch.FloatTensor(state).to(device)

            action_probs = self.policy.actor.forward(state)
            action_probs = action_probs * \
                torch.from_numpy(get_mask(2)).to(device)

            dist = Categorical(action_probs)

            action = dist.sample()
            return action.item()

    def select_action(self, state):
        """Select an appropriate action from the agent policy.

        Arguments:
            state {torch tensor} -- Current state of the environment.
            """


        if self.has_continuous_action_space:
            with torch.no_grad():
                state = torch.FloatTensor(state).to(device)
                action, action_logprob, state_val = self.policy_old.act(state)

            self.buffer.states.append(state)
            self.buffer.actions.append(action)
            self.buffer.logprobs.append(action_logprob)
            self.buffer.state_values.append(state_val)

            return action.detach().cpu().numpy().flatten()
        else:
            with torch.no_grad():
                state = torch.FloatTensor(state).to(device)
                action, action_logprob, state_val = self.policy_old.act(state)

            self.buffer.states.append(state)
            self.buffer.actions.append(action)
            self.buffer.logprobs.append(action_logprob)
            self.buffer.state_values.append(state_val)

            return action.item()

    def update(self):
        """--------------------------------------------------------------------------------------------
        Update actor and critic for K epochs on sampled batch:

        """
        # Monte Carlo estimate of returns
        rewards = []
        discounted_reward = 0
        for reward, is_terminal in zip(reversed(self.buffer.rewards), reversed(self.buffer.is_terminals)):
            if is_terminal:
                discounted_reward = 0
            discounted_reward = reward + (self.gamma * discounted_reward)
            rewards.insert(0, discounted_reward)

        # Normalizing the rewards
        rewards = torch.tensor(rewards, dtype=torch.float32).to(device)
        rewards = (rewards - rewards.mean()) / (rewards.std() + 1e-7)

        # convert list to tensor
        old_states = torch.squeeze(torch.stack(
            self.buffer.states, dim=0)).detach().to(device)
        old_actions = torch.squeeze(torch.stack(
            self.buffer.actions, dim=0)).detach().to(device)
        old_logprobs = torch.squeeze(torch.stack(
            self.buffer.logprobs, dim=0)).detach().to(device)
        old_state_values = torch.squeeze(torch.stack(
            self.buffer.state_values, dim=0)).detach().to(device)

        # calculate advantages
        advantages = rewards.detach() - old_state_values.detach()

        # Optimize policy for K epochs
        for _ in range(self.K_epochs):
            # Evaluating old actions and values
            logprobs, state_values, dist_entropy = self.policy.evaluate(
                old_states, old_actions)

            # match state_values tensor dimensions with rewards tensor
            state_values = torch.squeeze(state_values)

            # Finding the ratio (pi_theta / pi_theta__old)
            ratios = torch.exp(logprobs - old_logprobs.detach())

            # Finding Surrogate Loss
            surr1 = ratios * advantages
            surr2 = torch.clamp(ratios, 1 - self.eps_clip,
                                1 + self.eps_clip) * advantages

            # final loss of clipped objective PPO
            loss = -torch.min(surr1, surr2) + 0.5 * \
                self.MseLoss(state_values, rewards) - 0.01 * dist_entropy

            # take gradient step
            self.optimizer.zero_grad()
            loss.mean().backward()
            self.optimizer.step()

        # Copy new weights into old policy
        self.policy_old.load_state_dict(self.policy.state_dict())
        print('update')
        # clear buffer
        self.buffer.clear()

    def save(self, checkpoint_path):
        """Save model parameters to checkpoint

        Arguments:
            checkpoint_path {str} -- checkpoint path
        """
        torch.save(self.policy_old.state_dict(), checkpoint_path)

    def load(self, checkpoint_path):
        """Load model parameters from checkpoint

        Arguments:
            checkpoint_path {str} -- checkpoint path
        """
        self.policy_old.load_state_dict(torch.load(
            checkpoint_path, map_location=lambda storage, loc: storage))
        self.policy.load_state_dict(torch.load(
            checkpoint_path, map_location=lambda storage, loc: storage))
