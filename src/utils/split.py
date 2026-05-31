import numpy as np
import pandas as pd
from skmultilearn.model_selection import iterative_train_test_split


def multilabel_split(
    df: pd.DataFrame, 
    label_columns: list[str], 
    test_size: float, 
    val_size: float) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    
    feature_cols = df.drop(columns=label_columns).columns.tolist()
    X = df[feature_cols].values
    y = df[label_columns].values.astype(float)

    X_train, y_train, X_test, y_test = iterative_train_test_split(
        X, y, test_size=test_size
    )

    val_ratio = val_size / (1 - test_size)
    X_train, y_train, X_val, y_val = iterative_train_test_split(
        X_train, y_train, test_size=val_ratio
    )

    def to_df(X_part, y_part):
        df_x = pd.DataFrame(X_part, columns=feature_cols)
        df_y = pd.DataFrame(y_part, columns=label_columns).astype(int)
        return pd.concat([df_x.reset_index(drop=True), df_y.reset_index(drop=True)], axis=1)

    return to_df(X_train, y_train), to_df(X_val, y_val), to_df(X_test, y_test)