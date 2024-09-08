import json
from pathlib import Path

import openai


class TestGPT:
    def __init__(self, api_key, config_file="testgpt_prompting.json"):
        self.api_key = api_key

        self.config_file = config_file
        self.initial_parameters = self.get_initial_parameters()
        self.init_openai()

    def init_openai(self):
        openai.api_key = self.api_key
        # Dit zou een goede plek zijn om meer openai parameters te zetten

    def get_initial_parameters(self):
        self_path = Path(globals().get("__file__", "./_")).absolute().parent
        config_file = self_path / self.config_file
        with open(config_file) as f:
            return json.load(f)

    def _generate_question(self, note, question_type):
        if question_type not in self.initial_parameters["prompts"]:
            raise ValueError(
                f"Question type {question_type} not found in config file {self.config_file}"
            )
        if not note:
            raise ValueError("The given note was empty, we can't ask empty questions")
        parameters = {
            "model": self.initial_parameters["model"],
            "messages": self.initial_parameters["prompts"][question_type]["messages"],
        }
        parameters["messages"].append({"role": "user", "content": note})
        try:
            response = openai.ChatCompletion.create(**parameters)
            result = response["choices"][0]["message"]["content"]
        except Exception as e:
            print(e)
            result = None
        return result

    def generate_open_question(self, note):
        return self._generate_question(note, "open_question")

    def generate_multiple_choice_question(self, note):
        return self._generate_question(note, "multiple_choice_question")


if __name__ == "__main__":
    api_key = "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"
    test_gpt = TestGPT(api_key)
    test_text = """
De grutto is een oer-Hollandse weidevogel. Je vindt deze grote, slanke steltloper op erven en graslanden van
 boerenbedrijven waar voldoende ruimte is voor natuur. Het meest ideaal zijn vochtige, kruidenrijke graslanden met een
  goed bodemleven en volop insecten aan de oppervlakte.
"""
    result = test_gpt.generate_open_question(test_text)
    print(result)
    result = test_gpt.generate_multiple_choice_question(test_text)
    print(result)
