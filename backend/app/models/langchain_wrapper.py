import os
from dotenv import load_dotenv
from openai import OpenAI
import requests

load_dotenv()


class LangchainWrapper:
    def __init__(self):
        self.OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
        self.open_ai = OpenAI()

    def generate_completion(self, prompt: str):
        print("generating completion")

        response = self.open_ai.chat.completions.create(
            model='gpt-3.5-turbo',
            # model='gpt-4o',
            messages=[{
                "role": "user",
                "content": prompt
            }],
            max_tokens=700
        )
        text = response.choices[0].message.content.strip()
        return text

    def generate_photo(self, photo_prompt: str):
        improved_gpt_prompt = (
            f"A positive image of: {photo_prompt}, rendered artistically in a"
            " chic, cartooney, minimalistic style."
        )

        response = self.open_ai.images.generate(
            model="dall-e-3",
            prompt=improved_gpt_prompt,
            size="1024x1024",
            quality="standard",
            n=1,
        )
        image_url = response.data[0].url
        print("image url", image_url)
        img_data = requests.get(image_url).content
        return img_data


if __name__ == '__main__':
    wrapper = LangchainWrapper()
    wrapper.generate_photo("making money selling ebooks")
