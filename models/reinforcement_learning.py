import ray
from ray import tune
from ray.rllib.agents.ppo import PPOTrainer

def train_reinforcement_learning():
    ray.init(ignore_reinit_error=True)
    config = {
        "env": "CartPole-v1",
        "num_workers": 1,
        "framework": "torch",
    }
    trainer = PPOTrainer(config=config)
    for i in range(3):
        result = trainer.train()
        print(f"Iteration {i}: reward mean = {result['episode_reward_mean']}")
    ray.shutdown()

if __name__ == "__main__":
    train_reinforcement_learning()
