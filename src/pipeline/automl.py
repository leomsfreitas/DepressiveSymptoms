from dataclasses import dataclass
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pandas as pd

from src.models.automl import MultilabelPredictor
from src.utils.split import multilabel_split


@dataclass
class AutoGluonConfig:
    model_path: str | None = None
    label_columns: list[str] | None = None
    test_size: float = 0.15
    val_size: float = 20 / 85
    seed: int = 21
    presets: str = "high_quality"
    time_limit: int = 900
    gpu: int = 1
    eval_metrics: list[str] | None = None


class PipelineAutoGluon(MultilabelPredictor):
    def __init__(self, config: AutoGluonConfig, df: pd.DataFrame):
        self.config = config

        label_columns = config.label_columns if config.label_columns is not None else df.columns[1:-1].tolist()
        eval_metrics = config.eval_metrics if config.eval_metrics is not None else ["f1_macro"] * len(label_columns)

        super().__init__(labels=label_columns, eval_metrics=eval_metrics, path=config.model_path)

    def split(self, df: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        return multilabel_split(df, self.labels, self.config.test_size, self.config.val_size)

    def _build_reports_df(self, y_true: pd.DataFrame, y_pred: pd.DataFrame) -> pd.DataFrame:
        rows = []
        for label in self.labels:
            report_dict = classification_report(
                y_true[label], y_pred[label], output_dict=True, zero_division=0
            )
            report_df = pd.DataFrame(report_dict).T.reset_index().rename(columns={"index": "metric_or_class"})
            report_df.insert(0, "label", label)
            rows.append(report_df)

        out = pd.concat(rows, ignore_index=True)
        cols_to_round = ["precision", "recall", "f1-score"]
        out[cols_to_round] = out[cols_to_round].apply(pd.to_numeric, errors="coerce").round(4)
        return out

    def train(self, train_df: pd.DataFrame, val_df: pd.DataFrame) -> None:
        super().fit(
            train_data=train_df,
            ag_args_fit={'num_gpus': self.config.gpu},
            tuning_data=val_df,
            presets=self.config.presets,
            time_limit=self.config.time_limit,
        )

    def evaluate(self, test_df: pd.DataFrame) -> pd.DataFrame:
        y_pred = super().predict(test_df)
        y_true = test_df[self.labels]
        return self._build_reports_df(y_true, y_pred)

    def predict(self, df: pd.DataFrame) -> pd.DataFrame:
        return super().predict(df)