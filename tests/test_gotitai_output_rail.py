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

from aioresponses import aioresponses

from nemoguardrails import RailsConfig
from tests.utils import TestChat


def test_1(monkeypatch):
    # TODO add GotItAI's truthchecker url
    gotitai_api_url = ""
    monkeypatch.setenv("GOTITAI_API_KEY", "xxx")

    config = RailsConfig.from_content(
        colang_content="""
            define user express greeting
              "hi"

            define user ask general question
              "Do Unicorns live on Mars?"

            define flow
              user express greeting
              bot express greeting

            define bot express greeting
              "Hello! How can I assist you today?"
        """,
        yaml_content="""
            models:
              - type: main
                engine: openai
                model: gpt-3.5-turbo-instruct

            rails:
              output:
                flows:
                  - gotitai rag truthcheck
        """,
    )
    chat = TestChat(
        config,
        llm_completions=[
            "  express greeting",
            " ask general question",
            " express general response",
            "Yes, Unicorns do live in Mars.",
        ],
    )

    with aioresponses() as m:
        # output rail will not be activated
        chat >> "Hello!"
        chat << "Hello! How can I assist you today?"

        # Now, output rail will be activated
        m.post(
            gotitai_api_url,
            payload={
                "hallucination": "yes",
            },
        )

        chat >> "Do Unicorns live on Mars?"
        chat << "I'm sorry, I can't respond to that."
