# SPDX-FileCopyrightText: Copyright (c) 2023 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: Apache-2.0
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import json

import pandas as pd
import typer


def process_dataset(dataset_path: str, output_path: str):
    """
    Extracts the user input and the label from the openai moderation dataset.
    The dataset can be downloaded from Huggingface and it has to be unzipped.
    https://huggingface.co/datasets/mmathys/openai-moderation-api-evaluation

    Writes a processed jsonl file. The required output format can be found in ./processed_sample.jsonl
    """
    df = pd.read_csv(dataset_path)
    print(f"Original dataset sample:\n{df.head()}")
    # df = df.rename(columns={"model_output": "bot_response"})
    label_columns = df[["toxicity", "jailbreaking"]]
    df["user_input_label"] = label_columns.any(axis="columns")

    print(f"User input label distribution:\n{df['user_input_label'].value_counts()}")
    print(f"Modified dataset sample:\n{df.head()}")
    df.to_json(output_path, orient="records", lines=True)


def main(
    dataset_path: str = typer.Option(
        "./lmsys-toxic-chat/toxic-chat_annotation_all.csv",
        help="Path to the OpenAI moderation set",
    ),
):
    """
    Standardizes the openai moderation dataset to the format used by the Guardrails evaluation scripts.
    Writes a processed jsonl file. The required output format can be found in ./processed_sample.jsonl
    """
    process_dataset(dataset_path, output_path="./lmsys-toxic-chat/processed.jsonl")


if __name__ == "__main__":
    typer.run(main)
