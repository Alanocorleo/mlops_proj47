import os
import logging
import random

import hydra
import numpy as np
import torch
from happytransformer import HappyTextToText, TTTrainArgs
from omegaconf import DictConfig

os.environ["WANDB_PROJECT"] = "mlops-proj47"
os.environ["WANDB_LOG_MODEL"] = "checkpoint"

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

def set_seed(seed: int):
    """Helper function for reproducible behavior to set the seed in `random`, `numpy`, `torch` a
    Args:
        seed (`int`): The seed to set.
    """
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)

@hydra.main(config_path="../config", config_name="default_config.yaml", version_base=None)
def train(config: DictConfig) -> None:
    """ Train the model using the provided configuration. """
    cfg = config.training
    model = HappyTextToText("t5-small")
    args = TTTrainArgs(batch_size=cfg.batch_size, report_to="wandb",learning_rate= cfg.lr,num_train_epochs=cfg.epochs)
    set_seed(cfg.seed)
    logging.info("Training model...")
    model.train(cfg.dataset_path, args=args)
    logging.info("Training complete.")
    model.save("models/model/")
    logging.info("Model saved.")

if __name__ == "__main__":
    train()
