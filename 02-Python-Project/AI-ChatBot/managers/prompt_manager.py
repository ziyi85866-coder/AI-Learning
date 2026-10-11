import os


class PromptManager:

    def __init__(self, prompt_dir="prompts"):
        self.prompt_dir = prompt_dir

    def load_prompt(self, filename):

        path = os.path.join(
            self.prompt_dir,
            filename
        )

        with open(
                path,
                "r",
                encoding="utf-8"
        ) as f:

            return f.read()

    def build_prompt(self, filename, **kwargs):

        template = self.load_prompt(filename)

        return template.format(**kwargs)