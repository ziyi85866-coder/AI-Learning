import os
from dotenv import load_dotenv


class ConfigManager:

    def __init__(self):
        load_dotenv()

        self.api_key = os.getenv("ARK_API_KEY")
        self.base_url = os.getenv(
            "ARK_BASE_URL",
            "https://ark.cn-beijing.volces.com/api/coding/v3"
        )
        self.model = os.getenv(
            "ARK_MODEL",
            "deepseek-v4-1-flash-260910"
        )


        if not self.api_key or not self.api_key.strip():
            raise ValueError("缺少 ARK_API_KEY，请检查 .env 文件")