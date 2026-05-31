import pandas as pd
import transformers

import re
import json
import logging

from sklearn.preprocessing import MultiLabelBinarizer

from dataclasses import dataclass, field
from collections.abc import Callable
import torch

transformers.logging.set_verbosity_error()
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@dataclass
class ModelConfig:
    model_path: str
    label_classes: list
    max_new_tokens: int = 20
    do_sample: bool = False
    temperature: float | None = None
    top_p: float | None = None
    dtype: torch.dtype = torch.bfloat16
    device_map: str = "auto"
    kwargs: dict = field(default_factory=dict)
    model_name: str | None = None
    

@dataclass
class PromptConfig:
    system_prompt: str
    user_prompt: Callable[[str], str]
    batch_size: int
    text_col: str
    kwargs: dict = field(default_factory=dict)


class ChatTemplatePipeline:
    def __init__(self, config: ModelConfig):
        self.config = config
        self._pipeline = None
        self._tokenizer = None
        self._mlb = None

    def _load(self):
        if self._pipeline is not None:
            return

        self._pipeline = transformers.pipeline(
            "text-generation",
            model=self.config.model_path,
            dtype=self.config.dtype,
            device_map=self.config.device_map,
            **self.config.kwargs
        )

        self._tokenizer = self._pipeline.tokenizer

        self._gen_config = transformers.GenerationConfig(
            max_new_tokens=self.config.max_new_tokens,
            do_sample=self.config.do_sample,
            max_length=None,
            temperature=self.config.temperature,
            top_p=self.config.top_p,
            eos_token_id=self._tokenizer.eos_token_id
        )

        if self._mlb is None:
            self._mlb = MultiLabelBinarizer(classes=self.config.label_classes)
            self._mlb.fit([self.config.label_classes])

    def _build_prompt(self, text: str, prompt_cfg: PromptConfig) -> str:
        messages = [
            {"role": "system", "content": prompt_cfg.system_prompt},
            {"role": "user",   "content": prompt_cfg.user_prompt(text)},
        ]
        return self._tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True,
            **prompt_cfg.kwargs
        )

    def _parser_label(self, generated_text: str) -> str:
        try:
            match = re.search(r'\{.*?\}', generated_text, re.DOTALL)
            data = json.loads(match.group())
            labels = data.get("labels", [])

            if labels == [0]:
                return ""

            numbers = [
                str(n) for n in labels
                if str(n) in self.config.label_classes
            ]
            return ",".join(numbers)
        except Exception:
            return ""

    def _predict(self, texts: list[str], prompt_config: PromptConfig, verbose: bool) -> list[str]:
        prompts = [self._build_prompt(t, prompt_config) for t in texts]

        outputs = self._pipeline(
            prompts,
            generation_config=self._gen_config,
            return_full_text=False,
            batch_size=prompt_config.batch_size,
        )

        labels = []
        for i, output in enumerate(outputs):
            generated = output[0]["generated_text"]
            label = self._parser_label(generated)
            labels.append(label)

            if verbose:
                logger.debug("idx=%d | out=%r | parser=%s", i, generated, label)

        return labels

    def _encode(self, raw_labels: list[str]) -> pd.DataFrame:
        if self._mlb is None:
            self._mlb = MultiLabelBinarizer(classes=self.config.label_classes)
            self._mlb.fit([self.config.label_classes])

        split = [s.split(",") if s else [] for s in raw_labels]
        return pd.DataFrame(self._mlb.transform(split), columns=self._mlb.classes_)

    def run(self, df: pd.DataFrame, prompt_config: PromptConfig, verbose: bool = False) -> dict[str, list[str] | pd.DataFrame]:
        self._load()

        texts = df[prompt_config.text_col].tolist()
        labels = self._predict(texts, prompt_config, verbose)

        return {
            "labels": labels,
            "encoded": self._encode(labels)
        }