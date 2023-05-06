import os
from datetime import datetime
from ai.environment import SplendorEnv
import torch
import numpy as np
from model.game_manager import GameManager

from ai.model_ppo import PPO


################################### Training ###################################

def train():
    print("============================================================================================")

    ####### initialize environment hyperparameters ######
    env_name = "Splendor"
    game = GameManager(nbPlayer=2)
    has_continuous_action_space = False  # continuous action space; else discrete

    max_ep_len = 400  # max timesteps in one episode
    # break training loop if timeteps > max_training_timesteps
    max_training_timesteps = int(3e9)

    # print avg reward in the interval (in num timesteps)
    print_freq = max_ep_len * 5
    # log avg reward in the interval (in num timesteps)
    log_freq = max_ep_len * 5
    save_model_freq = int(10000)  # save model frequency (in num timesteps)

    # starting std for action distribution (Multivariate Normal)
    action_std = 0.6
    # linearly decay action_std (action_std = action_std - action_std_decay_rate)
    action_std_decay_rate = 0.05
    # minimum action_std (stop decay after action_std <= min_action_std)
    min_action_std = 0.1
    # action_std decay frequency (in num timesteps)
    action_std_decay_freq = int(2.5e5)
    #####################################################

    # Note : print/log frequencies should be > than max_ep_len

    ################ PPO hyperparameters ################
    update_timestep = max_ep_len * 10  # update policy every n timesteps
    K_epochs = 80  # update policy for K epochs in one PPO update

    eps_clip = 0.2  # clip parameter for PPO
    gamma = 0.99  # discount factor

    lr_actor = 0.0005  # learning rate for actor network
    lr_critic = 0.0002  # learning rate for critic network

    random_seed = 0  # set random seed if required (0 = no random seed)
    #####################################################

    print("training environment name : " + env_name)

    env: SplendorEnv = SplendorEnv(game)

    # state space dimension
    state_dim = env.observation_space._shape[0]

    # action space dimension
    if has_continuous_action_space:
        action_dim = env.action_space.shape[0]
    else:
        action_dim = env.action_space.n

    ###################### logging ######################

    # log files for multiple runs are NOT overwritten
    log_dir1 = "PPO_logs1"
    log_dir2 = "PPO_logs2"
    if not os.path.exists(log_dir1):
        os.makedirs(log_dir1)

    if not os.path.exists(log_dir2):
        os.makedirs(log_dir2)

    log_dir1 = log_dir1 + '/' + env_name + '/'
    log_dir2 = log_dir2 + '/' + env_name + '/'

    if not os.path.exists(log_dir1):
        os.makedirs(log_dir1)

    if not os.path.exists(log_dir2):
        os.makedirs(log_dir2)

    # get number of log files in log directory
    run_num = 0
    current_num_files1 = next(os.walk(log_dir1))[2]
    current_num_files2 = next(os.walk(log_dir2))[2]
    run_num1 = len(current_num_files1)
    run_num2 = len(current_num_files2)

    # create new log file for each run
    log_f_name1 = log_dir1 + '/PPO_' + env_name + "_log_" + str(run_num1) + ".csv"
    log_f_name2 = log_dir2 + '/PPO_' + env_name + "_log_" + str(run_num2) + ".csv"

    print("current logging run number for " + env_name + " : ", run_num)
    print("logging at : " + log_f_name1)
    #####################################################

    ################### checkpointing ###################
    # change this to prevent overwriting weights in same env_name folder
    run_num_pretrained = 0

    directory = "PPO_preTrained"
    if not os.path.exists(directory):
        os.makedirs(directory)

    directory1 = directory + '/' + env_name + '/' + str(1) + '/'
    directory2 = directory + '/' + env_name + '/' + str(2) + '/'
    if not os.path.exists(directory1):
        os.makedirs(directory1)
    if not os.path.exists(directory2):
        os.makedirs(directory2)

    checkpoint_path1 = directory1 + \
                       "PPO_{}_{}_{}.pth".format(env_name, random_seed, run_num_pretrained)
    checkpoint_path2 = directory2 + \
                       "PPO_{}_{}_{}.pth".format(env_name, random_seed, run_num_pretrained)
    print("save checkpoint path : " + checkpoint_path1)
    #####################################################

    ############# print all hyperparameters #############
    print("--------------------------------------------------------------------------------------------")
    print("max training timesteps : ", max_training_timesteps)
    print("max timesteps per episode : ", max_ep_len)
    print("model saving frequency : " + str(save_model_freq) + " timesteps")
    print("log frequency : " + str(log_freq) + " timesteps")
    print("printing average reward over episodes in last : " +
          str(print_freq) + " timesteps")
    print("--------------------------------------------------------------------------------------------")
    print("state space dimension : ", state_dim)
    print("action space dimension : ", action_dim)
    print("--------------------------------------------------------------------------------------------")
    if has_continuous_action_space:
        print("Initializing a continuous action space policy")
        print("--------------------------------------------------------------------------------------------")
        print("starting std of action distribution : ", action_std)
        print("decay rate of std of action distribution : ", action_std_decay_rate)
        print("minimum std of action distribution : ", min_action_std)
        print("decay frequency of std of action distribution : " +
              str(action_std_decay_freq) + " timesteps")
    else:
        print("Initializing a discrete action space policy")
    print("--------------------------------------------------------------------------------------------")
    print("PPO update frequency : " + str(update_timestep) + " timesteps")
    print("PPO K epochs : ", K_epochs)
    print("PPO epsilon clip : ", eps_clip)
    print("discount factor (gamma) : ", gamma)
    print("--------------------------------------------------------------------------------------------")
    print("optimizer learning rate actor : ", lr_actor)
    print("optimizer learning rate critic : ", lr_critic)
    if random_seed:
        print("--------------------------------------------------------------------------------------------")
        print("setting random seed to ", random_seed)
        torch.manual_seed(random_seed)
        env.seed(random_seed)
        np.random.seed(random_seed)
    #####################################################

    print("============================================================================================")

    ################# training procedure ################

    # initialize a PPO agent
    ppo_agent_1 = PPO(state_dim, action_dim, lr_actor, lr_critic, gamma, K_epochs, eps_clip,
                      has_continuous_action_space,
                      action_std,1)
    ppo_agent_2 = PPO(state_dim, action_dim, lr_actor, lr_critic,gamma, K_epochs, eps_clip,
                      has_continuous_action_space,
                      action_std,2)

    directory = "PPO_preTrained" + '/' + env_name + '/'
    checkpoint_path = directory + \
                      "PPO_{}_{}_{}.pth".format(env_name, random_seed, 0)
    print("loading network from : " + checkpoint_path)
    ppo_agent_1.load(checkpoint_path1)
    #ppo_agent_2.load(checkpoint_path2)
    # ppo_agent.load(checkpoint_path)

    # track total training time
    start_time = datetime.now().replace(microsecond=0)
    print("Started training at (GMT) : ", start_time)

    print("============================================================================================")

    # logging file
    log_f1 = open(log_f_name1, "w+")
    log_f2 = open(log_f_name2, "w+")

    log_f1.write('episode,timestep,reward\n')
    log_f2.write('episode,timestep,reward\n')
    #ppo_agent1.load(checkpoint_path1)

    # printing and logging variables
    print_running_reward = 0
    print_running_episodes = 0

    log_running_reward1 = 0
    log_running_episodes1 = 0

    log_running_reward2 = 0
    log_running_episodes2 = 0

    time_step = 0
    saving_timestep = 0
    i_episode = 0

    # training loop
    while time_step <= max_training_timesteps:

        state = env.reset()
        current_ep_reward1 = 0
        current_ep_reward2 = 0
        if i_episode % 300 == 0 and i_episode > 0:
            # Each 500 episode, load a new random pretrained model and play

            count_pretrained = len(os.listdir(directory2))
            if count_pretrained == 0:
                break
            # store the name of each file in a list
            files_names = []
            for filename in os.listdir(directory2):

                # remove PPO_Splendor_0 from the file name
                filename = filename.replace("PPO_Splendor_0_", "")
                # remove .pth from the file name
                filename = filename.replace(".pth", "")
                # add the file name to the list
                files_names.append(filename)
            # convert the list to a numpy array
            files_names = np.array(files_names)

            # select a random file name
            random_file_name = np.random.choice(files_names, 1)
            run_num_pretrained = directory2 + \
                                 "PPO_{}_{}_{}.pth".format(env_name, random_seed, run_num_pretrained)
            print("loading network from : " + checkpoint_path2)
            ppo_agent_2.load(checkpoint_path2)
        for t in range(1, max_ep_len + 1):

            # select action with policy
            if env.game.currentPlayer == 0:
                action = ppo_agent_1.select_action(state)
                state, reward, done, info = env.step(action)
                # saving reward and is_terminals
                ppo_agent_1.buffer.rewards.append(reward)
                ppo_agent_1.buffer.is_terminals.append(done)





            else:
                action = ppo_agent_2.select_action(state)
                state, reward, done, info = env.step(action)
                ppo_agent_2.buffer.rewards.append(reward)
                ppo_agent_2.buffer.is_terminals.append(done)
            if info['flag'] == 0:
                #print("player 1 win")
                ppo_agent_1.buffer.rewards[-1] = 1000/100
                ppo_agent_2.buffer.rewards[-1] = -1000/100
                current_ep_reward1 += 1000/100
                current_ep_reward2 -= 1000/100
            elif info['flag'] == 1:
                #print("player 2 win")
                ppo_agent_2.buffer.rewards[-1] = 1000/100
                ppo_agent_1.buffer.rewards[-1] = -1000/100
                current_ep_reward2 += 1000 / 100
                current_ep_reward1 -= 1000 / 100
            elif info['flag'] == 2:
                #print("draw")
                ppo_agent_1.buffer.rewards[-1] = 0
                ppo_agent_2.buffer.rewards[-1] = 0
                current_ep_reward1 += 0
                current_ep_reward2 -= 0
                reward = 0
            elif info['flag'] == 3 :
                #print("blocked")
                ppo_agent_1.buffer.rewards[-1] = -1500/100
                ppo_agent_2.buffer.rewards[-1] = -1500/100
                current_ep_reward1 -= 1500 / 100
                current_ep_reward2 -= 1500 / 100


            time_step += 1

            # update PPO agent
            if time_step % update_timestep == 0:
                ppo_agent_1.update()
                ppo_agent_2.update()
                break

            # if continuous action space; then decay action std of ouput action distribution
            if has_continuous_action_space and time_step % action_std_decay_freq == 0:
                ppo_agent_1.decay_action_std(
                    action_std_decay_rate, min_action_std)

            # log in logging file
            if time_step % log_freq == 0:
                print('LOGING')
                # log average reward till last episode
                log_avg_reward1 = log_running_reward1 / log_running_episodes1
                log_avg_reward1 = round(log_avg_reward1, 4)

                log_avg_reward2 = log_running_reward2 / log_running_episodes2
                log_avg_reward2 = round(log_avg_reward2, 4)

                log_f1.write('{},{},{}\n'.format(
                    i_episode, time_step, log_avg_reward1))
                log_f1.flush()

                log_running_reward1 = 0
                log_running_episodes1 = 0

                log_f2.write('{},{},{}\n'.format(
                    i_episode, time_step, log_avg_reward2))
                log_f2.flush()

                log_running_reward2 = 0
                log_running_episodes2 = 0

            # printing average reward
            if time_step % print_freq == 0:
                # print average reward till last episode
                print_avg_reward = print_running_reward / print_running_episodes
                print_avg_reward = round(print_avg_reward, 2)

                print("Episode : {} \t\t Timestep : {} \t\t Average Reward : {}".format(i_episode, time_step,
                                                                                        print_avg_reward))

                print_running_reward = 0
                print_running_episodes = 0

            # save model weights
            if time_step % save_model_freq == 0:
                print(
                    "--------------------------------------------------------------------------------------------")
                print("saving model at : " + checkpoint_path1 + " and " + checkpoint_path2)
                # if there are more than 10 saved models; then delete the oldest one
                if len(os.listdir(directory1)) >= 10:
                    os.remove(directory1 +
                              '/' + os.listdir(directory1)[0])
                if len(os.listdir(directory2)) >= 10:
                    os.remove(directory2 +
                              '/' + os.listdir(directory2)[0])
                # remove the .pth extension and add _actor critic.pth
                checkpoint_path1 = directory1 + \
                "PPO_{}_{}_{}.pth".format(env_name, random_seed, saving_timestep)

                checkpoint_path2 = directory2 + \
                "PPO_{}_{}_{}.pth".format(env_name, random_seed, saving_timestep)
                ppo_agent_1.save(checkpoint_path1,saving_timestep)
                ppo_agent_2.save(checkpoint_path2,saving_timestep)

                saving_timestep += 1
                saving_timestep = saving_timestep % 10

                print("Elapsed Time  : ", datetime.now().replace(
                    microsecond=0) - start_time)
                print(
                    "--------------------------------------------------------------------------------------------")
            if done:
                break

        print_running_reward += current_ep_reward1
        print_running_episodes += 1


        log_running_reward1 += current_ep_reward1
        log_running_episodes1 += 1
        log_running_reward2 += current_ep_reward2
        log_running_episodes2 += 1

        i_episode += 1


        # break; if the episode is over

    log_f1.close()
    log_f2.close()
    env.close()

    # print total training time
    print("============================================================================================")
    end_time = datetime.now().replace(microsecond=0)
    print("Started training at (GMT) : ", start_time)
    print("Finished training at (GMT) : ", end_time)
    print("Total training time  : ", end_time - start_time)
    print("============================================================================================")


if __name__ == '__main__':
    train()
