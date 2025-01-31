import os
from typing import Iterable

import torch
import transformers

from hnlp.utils import check_file
from hnlp.utils import convert_model_input, ModelInputType, device


class BertPretrainedModel:

    def __init__(self,
                 name: str,
                 model_path: str,
                 is_training: bool,
                 output_hidden_states: bool,
                 output_attentions: bool):
        self.name = name
        self.model_path = model_path
        self.is_training = is_training
        self.output_hidden_states = output_hidden_states
        self.output_attentions = output_attentions
        ConfigClass = getattr(transformers, self.name.title() + "Config")
        ModelClass = getattr(transformers, self.name.title() + "Model")
        config_path = os.path.join(self.model_path, "config.json")
        check_file(config_path)
        config = ConfigClass.from_json_file(config_path)
        config.output_hidden_states = self.output_hidden_states
        config.output_attentions = self.output_attentions
        if self.is_training:
            self.model = ModelClass.from_pretrained(self.model_path, config=config).to(
                device
            )
        else:
            self.model = ModelClass(config).to(device)

    # Here we use the `convert_model_input` mainly for those
    # who only want a pretrained model.
    @convert_model_input
    def call_batch(self, inputs: ModelInputType):
        """
        inputs element shape: [batch_size, seq_len]
        - if output_hidden_states and output_attentions is False. Outputs is a two elements tuple:
            - outputs[0] is the `last_hidden_state`
            - outputs[1] is the `pooled_output`
        - if both are True, Outputs is a four elements tuple:
            - outputs[0] and outputs[1] like before
            - outputs[2] is all_hidden_states,
              length = layer_num + 1(embedding output),
              all_hidden_states[-1] == outputs[0],
              shape is length * ([1, seq_len, hidden_size])
            - outputs[3] is all_attentions,
              length = layer_num,
              shape is length * ([1, attention_heads_num, seq_len, seq_len])
        """
        if self.is_training:
            outputs = self.model(**inputs)
        else:
            with torch.no_grad():
                outputs = self.model(**inputs)
        return outputs

    def __call__(self, inputs: Iterable):
        for batch in inputs:
            yield self.call_batch(batch)
