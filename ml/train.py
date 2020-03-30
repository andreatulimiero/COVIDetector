import glob
import json
import numpy as np
import os
import requests
import time
import torch
import urllib.request
import yaml

from collections import OrderedDict
from enum import Enum
from tensorboardX import SummaryWriter
from termcolor import colored
from tqdm import tqdm

import utils.accumulators
from utils.config import parse_cli_overides
from utils.data import AudioDataset
from models.covidetector import COVIDetector

config = OrderedDict(
    batch_size=10,
    channels=1,
    load_checkpoint_file=None,
    no_cuda=False,
    num_epochs=3,
    num_workers=1,
    max_samples=4, # Make it divisible by 2
    max_tokens=441000,
    seed=69,
    shuffle=True,
    split=0.6,
    sr=44100,

    # Dataset
    classification_dict = "./data/class.json",
    remote_url="http://18.156.30.58:8000/api/samples/", # Wherever the data is actually coming from.
    sound_folder="./data/",
    sound_ending=".wav",

    # Optimizer
    optimizer="Adam",
    learning_rate=0.0005,

    # Model Stuff
    hidden_act="gelu",

    conv1_in_ch=1,
    conv1_out_ch=8,
    conv1_kern=(1,11),
    conv1_stride=(1,6),
    pool1_kern=(1,3),
    pool1_stride=(1,2),

    conv2_out_ch=16,
    conv2_kern=(1,11),
    conv2_stride=(1,6),
    pool2_kern=(1,3),
    pool2_stride=(1,2),

    conv3_out_ch=64,
    conv3_kern=(1,11),
    conv3_stride=(1,6),
    pool3_kern=(1,3),
    pool3_stride=(1,2),

    conv4_kern=(3,4),
    conv4_stride=(1,2),
    pool4_kern=(2,2),
    pool4_stride=(2,2),

    conv5_kern=(1,3),
    conv5_stride=(1,2),
    pool5_kern=(1,2),
    pool5_stride=(1,1),

    reformer_attn_chunks=8,
    reformer_bucket_size=22,
    reformer_causal=True,
    reformer_depth=6,
    reformer_ff_chunks=200,
    reformer_max_seq_len=3200,
    reformer_n_hashes=4,
    reformer_num_mem_kv=128,
    reformer_heads=4,
    reformer_lsh_dropout=0.1,
    reformer_use_full_attn=False,


    final_linear=30,
    # Logging
    output_dir="./output",
)

output_dir = config["output_dir"]

def main():
    """
    Train a model
    You can either call this script directly (using the default params)
    or import it as a module, override config and run main()
    :return: scalar of the best accuracy
    """

    global output_dir
    output_dir = config["output_dir"]
    os.makedirs(output_dir, exist_ok=True)

    store_config()

    writer = SummaryWriter(log_dir=output_dir, max_queue=100, flush_secs=10)
    print("Tensorboard logs saved in '{}'".format(output_dir))

    torch.manual_seed(config["seed"])
    np.random.seed(config["seed"])

    device = torch.device("cuda" if not config["no_cuda"] and torch.cuda.is_available() else "cpu")

    training_loader, test_loader = get_dataset()
    model = get_model(device)

    if config["load_checkpoint_file"] is not None:
        restore_checkpoint(config["load_checkpoint_file"], model, device)

    max_steps = config["num_epochs"]

    optimizer, scheduler = get_optimizer(model.named_parameters())
    criterion = torch.nn.MSELoss()

    best_accuracy_so_far = utils.accumulators.Min()
    global_step = 0

    for epoch in range(config["num_epochs"]):
        print("Epoch {:04d}".format(epoch))
        model.train()

        writer.add_scalar("train/lr", scheduler.get_lr()[0], global_step)
        mean_train_accuracy = utils.accumulators.Mean()
        mean_train_loss = utils.accumulators.Mean()

        for batch_x, batch_y in tqdm(training_loader):
            batch_x, batch_y = batch_x.to(device), batch_y.to(device)

            prediction = model(batch_x)
            loss = criterion(prediction, batch_y)
            acc = accuracy(prediction, batch_y)

            loss.backward()
            optimizer.step()

            writer.add_scalar("train/loss", loss, global_step)
            writer.add_scalar("train/accuracy", acc, global_step)

            global_step += 1

            mean_train_loss.add(loss.item(), weight=len(batch_x))
            mean_train_accuracy.add(acc.item(), weight=len(batch_x))

        scheduler.step()

        log_metric("Mean_Difference", {"epoch": epoch, "value": mean_train_accuracy.value()}, {"split": "train"})
        log_metric("MSE_loss", {"epoch": epoch, "value": mean_train_loss.value()}, {"split": "train"})
        log_metric("lr", {"epoch": epoch, "value": scheduler.get_lr()[0]}, {})

        # Eval
        with torch.no_grad():
            model.eval()
            mean_test_accuracy = utils.accumulators.Mean()
            mean_test_loss = utils.accumulators.Mean()
            for batch_x, batch_y in test_loader:
                batch_x, batch_y = batch_x.to(device), batch_y.to(device)
                pred = model(batch_x)
                loss = criterion(pred, batch_y)
                acc = accuracy(pred, batch_y)
                mean_test_loss.add(loss.item(), weight=len(batch_x))
                mean_test_accuracy.add(acc.item(), weight=len(batch_x))

        log_metric("Mean_Difference", {"epoch": epoch, "value": mean_test_accuracy.value()}, {"split": "test"})
        log_metric("MSE_loss", {"epoch": epoch, "value": mean_test_loss.value()}, {"split": "test"})
        writer.add_scalar("eval/accuracy", mean_test_accuracy.value(), epoch)

        if best_accuracy_so_far.add(mean_test_accuracy.value()):
            store_checkpoint("best.checkpoint", model, epoch, mean_test_accuracy.value())

    store_checkpoint("final.checkpoint", model, config["num_epochs"]-1, mean_test_accuracy.value())
    writer.close()

    return best_accuracy_so_far.value()

def accuracy(predicted_logits, ref):
    """The mean error between the predicted and the ref"""
    diff = torch.flatten(predicted_logits) - torch.flatten(ref)
    # Lower is better
    return diff.abs().sum().float() / diff.shape[0]

def log_metric(name, values, tags):
    """
    Log timeseries data.
    Placeholder implementation.
    This function should be overwritten by any script that runs this as a module.
    """
    print("{name}: {values} ({tags})".format(name=name, values=values, tags=tags))

def get_dataset():
    """
    Downloads data if not already downloaded, and creates loaders.
    """
    if config["remote_url"] is not None:
        print("Retrieving data from remote source.")
        os.makedirs(config["sound_folder"], exist_ok=True)
        class_dict = {}
        req = requests.get(config["remote_url"])
        all_data = req.json()
        for sample in all_data:
            file_name = "{}_{}{}".format(sample["patient"], sample["created_at"], config["sound_ending"])
            urllib.request.urlretrieve(sample["url"], "{}{}".format(config["sound_folder"],file_name))
            class_dict[file_name] = sample["sick"]
        json_dict = json.dumps(class_dict)
        with open(config["classification_dict"], "w+") as f:
            f.write(json_dict)

    all_sound_files = [data for data in os.listdir(config["sound_folder"]) if data.endswith(config["sound_ending"])]
    all_sound_files.sort()
    files = []
    current_patient = all_sound_files[0].split("_")[0]
    patient_audio_samples = []

    for file_name in all_sound_files:
        split_file = file_name.split("_")
        new_patient = split_file[0]
        if new_patient != current_patient:
            current_patient = new_patient
            files.append(patient_audio_samples)
            patient_audio_samples = []
        patient_audio_samples.append(file_name)

    files.append(patient_audio_samples)
    split_idx = int(config["split"] * len(files))
    train_files = files[:split_idx]
    test_files = files[split_idx:]

    with open(config["classification_dict"]) as f:
        class_dict = json.load(f)

    train_dataset = AudioDataset(config, train_files, class_dict)
    test_dataset = AudioDataset(config, test_files, class_dict)

    train_loader = torch.utils.data.DataLoader(
        train_dataset,
        batch_size=config["batch_size"],
        shuffle=config["shuffle"],
        num_workers=config["num_workers"]
    )

    test_loader = torch.utils.data.DataLoader(
        test_dataset,
        batch_size=config["batch_size"],
        shuffle=config["shuffle"],
        num_workers=config["num_workers"]
    )

    return train_loader, test_loader

def get_model(device):
    """
    :param device: instance of torch.device
    :return: instance of torch.nn.Module
    """
    model = COVIDetector(config)
    model.to(device)
    if device == torch.device("cuda"):
        # For multi-gpu
        model = torch.nn.DataParallel(model)
        torch.backends.cudnn.benchmark=True

    return model

def get_optimizer(model_named_parameters):
    """
    Creates an optimizer for a given model
    :param model_parameters: a list of parameters to be trained
    :return: (optimizer, scheudler)
    """
    if config["optimizer"] == "Adam":
        model_named_parameters = OrderedDict(model_named_parameters)
        optimizer = torch.optim.Adam(model_named_parameters.values(), lr=config["learning_rate"])
    else:
        raise ValueError("Optimizer not yet implemented")
    scheduler = torch.optim.lr_scheduler.LambdaLR(optimizer, lr_lambda=lambda e: 1.0)

    return optimizer, scheduler

def store_config():
    path = os.path.join(output_dir, "config.yaml")
    with open(path, "w") as f:
        yaml.dump(dict(config), f)

def store_checkpoint(filename, model, epoch, test_accuracy):
    """Store a checkpoint file to the output directory"""
    path = os.path.join(output_dir, filename)

    # Ensure the output directory exists
    directory = os.path.dirname(path)
    if not os.path.isdir(directory):
        os.makedirs(directory, exist_ok=True)

    # remove buffer from checkpoint
    # TODO should not hard code
    def keep_state_dict_keys(key):
        if "self.R" in key:
            return False
        return True

    time.sleep(
        1
    )  # workaround for RuntimeError('Unknown Error -1') https://github.com/pytorch/pytorch/issues/10577
    torch.save(
        {
            "epoch": epoch,
            "test_accuracy": test_accuracy,
            "model_state_dict": OrderedDict([
                (key, value) for key, value in model.state_dict().items() if keep_state_dict_keys(key)
            ]),
        },
        path,
    )

def restore_checkpoint(fname, model, device):
    """Load a model from a checkpoint"""
    print("Loading {}".format(fname))
    with open(fname, "rb") as f:
        checkpoint_data = torch.load(f, map_location=device)

    try:
        model.load_state_dict(checkpoint_data["model_state_dict"])
    except RuntimeError as e:
        print(colored("Missing state_dict keys in checkpoint", "red"), e)
        print("Retrying...")
        state = model.state_dict()
        state.update(checkpoint_data["model_state_dict"])
        model.load_state_dict(state)

if __name__ == "__main__":
    config = parse_cli_overides(config)
    main()
