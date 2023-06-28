from __future__ import annotations
import os
import logging
import json
from poecaller import LangPoeCaller as PoeCaller

logger = logging.getLogger(__name__)

dir_path = os.path.dirname(os.path.realpath(__file__))

SECTRETS = f"{dir_path}/../secrets.json"
with open(SECTRETS) as f:
    secrets = json.load(f)


class AI:
    def __init__(self, model="chinchilla", **kwargs):
        self.bot_codename = model
        self.poe_caller = PoeCaller(secrets["POE_TOKEN"])

    def start(self, system, user):
        messages = [
            self.fsystem(system),
            self.fuser(user),
        ]

        return self.next(messages)

    def fsystem(self, msg):
        return {"role": "system", "content": msg}

    def fuser(self, msg):
        return {"role": "user", "content": msg}

    def fassistant(self, msg):
        return {"role": "assistant", "content": msg}

    def next(self, messages: list[dict[str, str]], prompt=None):
        if prompt:
            messages += [self.fuser(prompt)]

        logger.debug(f"Creating a new chat completion: {messages}")
        responses = self.poe_caller.chat(
            self.bot_codename,
            [msg["content"] for msg in messages if msg["role"] == "user"],
        )

        chat = []
        for response in responses:
            print(response, end="")
            chat.append(response)
        print()
        messages += [self.fassistant("".join(chat))]
        logger.debug(f"Chat completion finished: {messages}")
        return messages


def fallback_model(model: str) -> str:
    assert model in ["chinchilla", "a2"], f"Unknown model: {model}"
    return model
