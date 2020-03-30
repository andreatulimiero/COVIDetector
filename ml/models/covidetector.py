import torch
import torch.nn as nn
import torch.nn.functional as F

from reformer_pytorch import Reformer

class COVIDetector(nn.Module):
    """
    Takes in an audio sample, convolves it, runs it through a reformer,
    then outputs a class probability.
    """
    def __init__(self, config):
        super(COVIDetector, self).__init__()
        self.num_classes = config["max_samples"]
        if config["hidden_act"] == "gelu":
            self.act_func = F.gelu
        else:
            print("Activation function not found. Falling back on ReLU")
            self.act_func = F.relu

        self.conv_1 = nn.Conv2d(config["conv1_in_ch"],
                                config["conv1_out_ch"],
                                config["conv1_kern"],
                                stride=config["conv1_stride"])

        self.max_1 = nn.MaxPool2d(config["pool1_kern"],
                                  stride=config["pool1_stride"])

        self.conv_2 = nn.Conv2d(config["conv1_out_ch"],
                                config["conv2_out_ch"],
                                config["conv2_kern"],
                                stride=config["conv2_stride"])

        self.max_2 = nn.MaxPool2d(config["pool2_kern"],
                                  stride=config["pool2_stride"])

        self.conv_3 = nn.Conv2d(config["conv2_out_ch"],
                                config["conv3_out_ch"],
                                config["conv3_kern"],
                                stride=config["conv3_stride"])

        self.max_3 = nn.MaxPool2d(config["pool3_kern"],
                                  stride=config["pool3_stride"])

        self.reformer = Reformer(
                            attn_chunks = config["reformer_attn_chunks"],
                            bucket_size = config["reformer_bucket_size"],
                            causal = config["reformer_causal"],
                            dim = config["conv3_out_ch"],
                            depth = config["reformer_depth"],
                            ff_chunks = config["reformer_ff_chunks"],
                            heads = config["reformer_heads"],
                            lsh_dropout = config["reformer_lsh_dropout"],
                            max_seq_len = config["reformer_max_seq_len"],
                            n_hashes = config["reformer_n_hashes"],
                            num_mem_kv = config["reformer_num_mem_kv"], #all-attention paper
                            use_full_attn = config["reformer_use_full_attn"]) # TODO: See if adding .cuda() to the end is necessary

        self.conv_4 = nn.Conv2d(config["conv3_out_ch"],
                                config["conv2_out_ch"],
                                config["conv4_kern"],
                                stride=config["conv4_stride"])

        self.max_4 = nn.MaxPool2d(config["pool4_kern"],
                                  stride=config["pool4_stride"])

        self.conv_5 = nn.Conv2d(config["conv2_out_ch"],
                                config["conv1_in_ch"],
                                config["conv5_kern"],
                                stride=config["conv5_stride"])

        self.max_5 = nn.MaxPool2d(config["pool5_kern"],
                                  stride=config["pool5_stride"])



        self.linear = nn.Linear(config["final_linear"], self.num_classes)

    def forward(self, tensor):
        """
        Assume that the input tensor is already reshaped correctly
        That is, the shape is (batch_size, ch, tokens)
        | Convolve the input tensor
        | Pass convolved representation into the reformer
        | Sample it down
        """
        tensor = self.act_func(self.conv_1(tensor))
        tensor = self.max_1(tensor)
        tensor = self.act_func(self.conv_2(tensor))
        tensor = self.max_2(tensor)
        tensor = self.act_func(self.conv_3(tensor))
        tensor = self.max_3(tensor)

        # Reformer expects (batch_size, max_samples*max_tokens, ch)
        batch_size, ch, sampl, tok = tensor.shape
        tensor = tensor.permute(0,2,3,1).reshape(batch_size, sampl*tok, ch)
        tensor = self.reformer(tensor)
        tensor = tensor.reshape(batch_size, sampl, tok, ch).permute(0,3,1,2)

        # Now that positions have been attended to, can safely convolve to size (batch_size, max_tokens).
        tensor = self.act_func(self.conv_4(tensor))
        tensor = self.max_4(tensor)
        tensor = self.act_func(self.conv_5(tensor))
        tensor = self.max_5(tensor)

        # Contract, to fully connected.
        batch_size, ch, sampl, tok = tensor.shape
        tensor = tensor.reshape(batch_size, ch*sampl*tok)

        tensor = self.linear(tensor)

        return tensor
