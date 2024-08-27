from discord_webhook import DiscordWebhook
from os import path, makedirs, getenv
from re import findall, sub, escape
from requests import post
from time import sleep
from base64 import b64decode
import threading
from dotenv import load_dotenv

load_dotenv()

ANALYZED_URL = 'https://codes.thisisnotawebsitedotcom.com/'
with open("codes.txt", "r") as f:
        codes = f.read().splitlines()
codes = list(map(lambda code: sub(r'[^a-z0-9\?]', '', code.lower()), codes))

DEFAULT_MAX_ATTEMPTS = 1000
max_attempts = getenv('MAX_REQUESTS') or DEFAULT_MAX_ATTEMPTS
try:
        max_attempts = int(max_attempts)
except ValueError:
        print(f"Wrong data type for MAX_REQUESTS, using default instead ({DEFAULT_MAX_ATTEMPTS}).")
        max_attempts = DEFAULT_MAX_ATTEMPTS

webhook_url = getenv('WEBHOOK_URL')
while not webhook_url or not webhook_url.startswith('http'):
        webhook_url = str(input("Please enter the Discord webhook URL: "))

HEADERS = {
        "Accept": "*/*",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36",
        "Content-Type": "multipart/form-data; boundary=kljmyvW1ndjXaOEAg4vPm6RBUqO6MC5A" 
}

with open("template.html", "r", encoding="utf-8") as f:
        html_template = f.read()

def save_base64_image(base64_str: str, image_format: str, code: str, image_name: str = "image") -> str:
        directory = path.join("codes", code, "assets")
        image_filename = f"{image_name}.{image_format}"
        image_path = path.join(directory, image_filename)
        
        makedirs(directory, exist_ok=True)

        image_data = b64decode(base64_str)

        with open(image_path, "wb") as f:
                f.write(image_data)
        
        return rf"\{image_path}"

def process_html(html_string: str, code: str) -> str:
        base64_img_pattern = r'data:image/(png|jpeg);base64,([^"]+)'

        matches = findall(base64_img_pattern, html_string)

        new_html = html_string

        for i, (image_format, base64_img) in enumerate(matches, start=1):
                image_filename = save_base64_image(base64_img, image_format, code, f"image_{i}")

                replacement_text = rf"{image_filename}"

                new_html = sub(f'data:image/{image_format};base64,{escape(base64_img)}', replacement_text.replace('\\', r'\\'), new_html, count=1)

        return new_html

def save_file(content: bytes, content_type: str, index: int) -> str:
        directory = path.join("codes", code)
        data = content_type.split('/')
        file_type = data[0]
        file_extension = data[1]
        filename = f"{file_type}_{index}.{file_extension}"
        file_path = path.join(directory, filename)

        makedirs(directory, exist_ok=True)

        with open(file_path, 'wb') as f:
                f.write(content)
        
        return file_path

webhook = DiscordWebhook(url=webhook_url, username="Unique Responses Detector (by Brute Force)")

def code_analyzer(code: str):
        attempts = 0
        payload = f"--kljmyvW1ndjXaOEAg4vPm6RBUqO6MC5A\r\nContent-Disposition: form-data; name=\"code\"\r\n\r\n{code}\r\n--kljmyvW1ndjXaOEAg4vPm6RBUqO6MC5A--\r\n"
        unique_responses = []

        message = f"### Successfully started requesting... `{ANALYZED_URL}` with keyword `{code}`"
        print(message)
        webhook.content = message
        webhook.execute()

        while attempts < max_attempts:
                sleep(0.01)
                attempts += 1
                print(f"({code}) ", end='')
                try:
                        r = post(ANALYZED_URL, data=payload, headers=HEADERS)
                except Exception as e:
                        message = f"{str(attempts).zfill(3)} - Failed to fetch the URL: {e}"
                        print(message)
                        webhook.content = message
                        webhook.execute()
                        continue

                if r.status_code == 404:
                        message  = f"## `{code}` is an invalid keyword"
                        print(message)
                        webhook.content = message
                        webhook.execute()
                        break

                if r.status_code != 200:
                        message = f"{str(attempts).zfill(3)} - The server responded: {r.status_code}"
                        print(message)
                        webhook.content = message
                        webhook.execute()
                        try:
                                print(r.content)
                                webhook.content = r.content
                                webhook.execute()
                        finally:
                                continue
                
                content_type = r.headers.get('Content-Type', '')
                response = r.content
                
                if not 'text/html' in content_type:
                        if response in unique_responses:
                                message = f"{str(attempts).zfill(3)} - "
                                print(message)
                                continue

                        unique_responses.append(response)

                        file_path = save_file(response, content_type, len(unique_responses))
                        
                        message = f"{str(attempts).zfill(3)} - New unique response ({len(unique_responses)}): file saved as `{file_path}`"
                        print(message)
                        webhook.content = message
                        webhook.execute()
                        webhook.content = "Actual file:"
                        webhook.add_file(file=response, filename=file_path)
                        webhook.execute()
                        webhook.remove_files()
                        continue
                
                response = process_html(response.decode('utf-8'), code)

                if response in unique_responses:
                        message = f"{str(attempts).zfill(3)} - "
                        print(message)
                        continue
                
                unique_responses.append(response)
                directory = path.join("codes", code)
                filename = f"{code}_{len(unique_responses)}.html"
                file_path = path.join(directory, filename)

                makedirs(directory, exist_ok=True)

                with open(file_path, "w", encoding="utf-8") as f:
                        f.write(html_template.replace("{{NEW_BODY}}", response).replace("{{CODE}}", code).replace("hidden", ""))
                
                chunked_response = [response[i:i + 2000 - 10] for i in range(0, len(response), 2000 - 10)] if len(response) > 2000 - 10 else [response]
                message = f"{str(attempts).zfill(3)} - New unique response ({len(unique_responses)}):"
                print(message)
                webhook.content = message
                webhook.execute()
                
                for chunk in chunked_response:
                        print(chunk)
                        webhook.content = f"```\n{chunk}\n```"
                        webhook.execute()
                        sleep(1)

        message = f"End of the attempts for {code}."
        print(message)
        webhook.content = message
        webhook.execute()

def forLoop():
        for code in codes:
                code_analyzer(code)
        
        message = "End of the code."
        print(message)
        webhook.content = message
        webhook.execute()

def main():
        thread = threading.Thread(target=forLoop)
        thread.start()
        try:
                while True:
                        sleep(60)
        finally:
                message = "Main Python file is finished (threads not included)."
                print(message)
                webhook.content = message
                webhook.execute()

if __name__ == "__main__":
        main()
