from back.model import SplendorEnv

env = SplendorEnv()


print(env.action_space.n)
print(env.observation_space._shape[0])
