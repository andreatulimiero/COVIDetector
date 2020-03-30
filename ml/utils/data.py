from torch.utils.data import Dataset
import torch

import glob
import numpy as np
import librosa

class AudioDataset(Dataset):
    """
    Dataset to work with audio samples
    Preprocessing is done here.
    """

    def __init__(self, config, data_files, class_dict):
        """
        self.data_files will be a list of list of audio files from the same user.
        :input data_files: A list of list of individuals' audio recordings
        :input class_dict: A dictionary from {file_name: sick_bool}
        """
        self.data_files = data_files
        self.class_dict = class_dict
        self.sr = config["sr"]
        self.data_folder = config["sound_folder"]
        self.max_samples = config["max_samples"]
        self.max_tokens = config["max_tokens"]
        self.ch = config["channels"]

    def preprocess(self, sample):
        """
        Preprocessing done to the sample.
        :input sample: A voice sample, in the shape of a numpy array
        """
        if len(sample) < self.max_tokens:
            npad = ((0, self.max_tokens - len(sample)))
            sample = np.pad(sample, pad_width=npad, mode="constant", constant_values=0)
        elif len(sample) > self.max_tokens:
            sample = sample[:self.max_tokens]
        # TODO: More stuff here, in the future.
        return sample

    def __getitem__(self, item):
        data_samples = self.data_files[item]

        data = np.zeros((self.ch, self.max_samples, self.max_tokens))
        target = np.zeros(self.max_samples)
        for idx, sample in enumerate(data_samples):
            if idx >= self.max_samples:
                break
            audio_sample, _ = librosa.load("{}{}".format(self.data_folder, sample), sr=self.sr)
            audio_sample = self.preprocess(audio_sample)
            data[0][idx] = audio_sample
            target[idx] = int(self.class_dict[sample])

        return torch.tensor(data).float(), torch.tensor(target).float()

    def __len__(self):
        return len(self.data_files)
