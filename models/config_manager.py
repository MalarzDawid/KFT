from pathlib import Path
import json
import logging
from gpt import get_ai_request, create_prompt, AnswersModel
from constants import CONFIG_PATH, QUESTIONS
from utils import load_json_file

logger = logging.getLogger(__name__)

class ConfigManager:
    """Manages game configuration loading and saving."""
    def __init__(self):
        self.config = self.load_config()
        logger.info("ConfigManager initialized")

    def load_config(self):
        """Load the configuration from file."""
        try:
            config = load_json_file(CONFIG_PATH)
            logger.info(f"Configuration loaded from {CONFIG_PATH}")
            return config
        except FileNotFoundError:
            logger.warning(f"Config file {CONFIG_PATH} not found, using default")
            return {"questions": [], "bg_img": "None", "bg_color": [60, 30, 30], "prompt": "", "music": ""}

    def save_config(self, prompt, music, bg_img, bg_color, answer_counts):
        """Save the configuration to file."""
        data = {
            "prompt": prompt,
            "music": music,
            "bg_img": bg_img,
            "bg_color": list(bg_color),
            "questions": [
                {"text": q, "num_answers": n, "answers": self.config["questions"][i]["answers"] if i < len(self.config["questions"]) else []}
                for i, (q, n) in enumerate(zip(QUESTIONS, answer_counts))
            ]
        }
        try:
            with Path(CONFIG_PATH).open('w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            self.config = data
            logger.info(f"Configuration saved to {CONFIG_PATH}")
        except IOError as e:
            logger.error(f"Error saving config: {e}")
            raise

    def generate_ai_answers(self, universe):
        """Generate AI answers for the questions."""
        prompt = create_prompt(universe)
        try:
            answers = get_ai_request(prompt)
            for i, field_name in enumerate(answers.model_dump().keys()):
                if i < len(self.config["questions"]):
                    self.config["questions"][i]["answers"] = answers.__getattribute__(field_name)
            logger.info("AI answers generated")
        except Exception as e:
            logger.error(f"Error generating AI answers: {e}")
            raise
