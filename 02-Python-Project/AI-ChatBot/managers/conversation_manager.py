import json


class ConversationManager:

    def __init__(
            self,
            system_prompt,
            file_path="messages.json"
    ):
        self.system_prompt = system_prompt
        self.file_path = file_path

    def load_messages(self):

        try:
            with open(
                    self.file_path,
                    "r",
                    encoding="utf-8"
            ) as file:

                return json.load(file)

        except:

            return [
                {
                    "role": "system",
                    "content": self.system_prompt
                }
            ]

    def save_messages(self, messages):

        with open(
                self.file_path,
                "w",
                encoding="utf-8"
        ) as file:

            json.dump(
                messages,
                file,
                ensure_ascii=False,
                indent=4
            )

    def clear_messages(self):

        messages = [
            {
                "role": "system",
                "content": self.system_prompt
            }
        ]

        self.save_messages(messages)

        return messages