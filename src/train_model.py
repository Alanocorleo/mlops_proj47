import os

import hydra
from happytransformer import HappyTextToText, TTSettings, TTTrainArgs
from omegaconf import DictConfig


os.environ["WANDB_PROJECT"] = "mlops-proj47"
os.environ["WANDB_LOG_MODEL"] = "checkpoint"


@hydra.main(config_path="models/config", config_name="config.yaml")
def train(cfg: DictConfig) -> None:
    """ Train the model using the provided configuration. """
    model = HappyTextToText("t5-small")
    args = TTTrainArgs(batch_size=cfg.batch_size, report_to="wandb")

    model.train(cfg.dataset_path, args=args)
    beam_settings = TTSettings(num_beams=5, min_length=1, max_length=100)
    input_text_1 = "grammar: I I wants to codes."
    output_text_1 = model.generate_text(input_text_1, args=beam_settings)
    print(output_text_1.text)
    model.train(cfg.dataset_path, args=args)
    output_text_1 = model.generate_text(input_text_1, args=beam_settings)
    print(output_text_1.text)
    model.save("models/model/")


if __name__ == "__main__":
    train()
