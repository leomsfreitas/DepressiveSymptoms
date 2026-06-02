import pandas as pd
import numpy as np
import torch
from dataclasses import dataclass, field
from sklearn.metrics import classification_report
from datasets import Dataset

from transformers import (
    BertConfig,
    BertTokenizer,
    EarlyStoppingCallback,
    Trainer,
    TrainingArguments
    )

from src.models.bert import BertForMultiTaskClassification
from src.utils.split import multilabel_split


@dataclass
class BertMultilabelConfig:
    model_path: str
    label_columns: list[str]
    bert_model: str = "neuralmind/bert-large-portuguese-cased"
    max_length: int = 128
    train_args: dict = field(default_factory=dict)
    early_stopping: dict = field(default_factory=lambda: {"early_stopping_patience": 3})
    test_size: float = 0.15
    val_size: float = 20 / 85
    seed: int = 21


class PipelineBertMultilabel:
    def __init__(self, config: BertMultilabelConfig):
        self.config = config
        self.tokenizer = BertTokenizer.from_pretrained(config.bert_model)

    def split(self, df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        return multilabel_split(df, self.config.label_columns, self.config.test_size, self.config.val_size)

    def _make_dataset(self, df: pd.DataFrame, text_column: str, with_labels: bool = True) -> Dataset:
        encodings = self.tokenizer(
            df[text_column].tolist(),
            padding="max_length",
            truncation=True,
            max_length=self.config.max_length,
        )
        data = dict(encodings)
        if with_labels:
            data["labels"] = df[self.config.label_columns].values.tolist()
        return Dataset.from_dict(data).with_format("torch")

    def _build_model(self) -> BertForMultiTaskClassification:
        bert_cfg = BertConfig.from_pretrained(
            self.config.bert_model,
            num_labels=len(self.config.label_columns),
        )
        return BertForMultiTaskClassification.from_pretrained(self.config.bert_model, config=bert_cfg)

    def _compute_metrics(self, pred) -> dict:
        logits, labels = pred
        logits = torch.sigmoid(torch.tensor(logits))
        preds = (logits > 0.6).numpy().astype(int)

        metrics = {}
        all_precision, all_recall, all_f1 = [], [], []

        for task_idx, col in enumerate(self.config.label_columns):
            report = classification_report(
                labels[:, task_idx],
                preds[:, task_idx],
                labels=[0, 1],
                output_dict=True,
                zero_division=0,
            )
            macro = report["macro avg"]
            metrics[f"{col}_precision"] = round(macro["precision"], 4)
            metrics[f"{col}_recall"] = round(macro["recall"], 4)
            metrics[f"{col}_f1"] = round(macro["f1-score"], 4)
            metrics[f"{col}_support"] = int(report["1"]["support"])

            all_precision.append(macro["precision"])
            all_recall.append(macro["recall"])
            all_f1.append(macro["f1-score"])

        metrics["macro_avg_precision"] = round(np.mean(all_precision), 4)
        metrics["macro_avg_recall"] = round(np.mean(all_recall), 4)
        metrics["macro_avg_f1"] = round(np.mean(all_f1), 4)

        return metrics

    def train(self, train_df: pd.DataFrame, val_df: pd.DataFrame, text_column: str) -> Trainer:
        train_dataset = self._make_dataset(train_df, text_column)
        val_dataset = self._make_dataset(val_df, text_column)
        model = self._build_model()

        training_args = TrainingArguments(
            output_dir=self.config.model_path,
            **self.config.train_args,
        )
        trainer = Trainer(
            model=model,
            args=training_args,
            train_dataset=train_dataset,
            eval_dataset=val_dataset,
            compute_metrics=self._compute_metrics,
            callbacks=[EarlyStoppingCallback(**self.config.early_stopping)],
        )
        trainer.train()
        return trainer

    def evaluate(self, trainer: Trainer, df: pd.DataFrame, text_column: str) -> dict:
        dataset = self._make_dataset(df, text_column)
        pred_output = trainer.predict(dataset)
        preds = (torch.sigmoid(torch.tensor(pred_output.predictions)) > 0.6).int().numpy()
        report = classification_report(
            pred_output.label_ids,
            preds,
            target_names=self.config.label_columns,
            output_dict=True,
            zero_division=0,
        )
        return pd.DataFrame(report).T

    def predict(self, trainer: Trainer, df: pd.DataFrame, text_column: str) -> pd.DataFrame:
        dataset = self._make_dataset(df, text_column, with_labels=False)
        logits = trainer.predict(dataset).predictions
        preds = (torch.sigmoid(torch.tensor(logits)) > 0.6).int().numpy()
        return pd.DataFrame(preds, columns=self.config.label_columns, index=df.index)

    def save(self, trainer: Trainer):
        trainer.model.save_pretrained(self.config.model_path)
        self.tokenizer.save_pretrained(self.config.model_path)
