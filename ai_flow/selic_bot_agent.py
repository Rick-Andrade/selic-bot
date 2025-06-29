from openai import OpenAI
from ai_flow.agent_base import AgentBase
from ai_flow.prompt_paths import SELIC_PROMPT
import json
import os
import pdfplumber
import requests

class SelicAgent(AgentBase):
    def __init__(self, api_key: str, model: str = "gpt-4", prompt_path: str = SELIC_PROMPT):
        self.report_text = self._download_and_extract_copom_report()
        super().__init__(api_key=api_key, prompt_path=prompt_path, model=model)
        self.system_prompt = self._inject_context_into_prompt(self.system_prompt)

    def _build_client(self):
        return OpenAI(api_key=self.api_key)

    def _inject_context_into_prompt(self, prompt_template: str) -> str:
        return prompt_template.replace("{{RELATORIO_COPOM}}", self.report_text)

    def generate(self) -> str:
        if self.report_text == "":
            return "No Copom report available for analysis."
        
        messages = [
            {"role": "system", "content": self.system_prompt},
            {"role": "user", "content": "Analise o relatório mais recente do Copom e comente as tendências da taxa Selic."}
        ]
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            temperature=0.5,
        )
        content = response.choices[0].message.content
        return content.strip() if content else ""

    def _download_and_extract_copom_report(self) -> str:
        print("📎 Looking for the latest valid report based on a map of known dates...")

        minutes = {
            275: "20251210",
            274: "20251105",
            273: "20250917",
            272: "20250730",
            271: "20250618",
            270: "20240508",
            269: "20240320",
            268: "20240201",
            267: "20231213",
            266: "20231101",
        }

        history_file = "last_minute_read.json"
        if os.path.exists(history_file):
            with open(history_file, "r") as f:
                last_minute_read = json.load(f).get("last_minute_read", 0)
        else:
            last_minute_read = 0

        for number, data in sorted(minutes.items(), reverse=True):
            if number <= last_minute_read:
                print(f"ℹ️ Minute {number} has already been read previously. Skipping.")
                continue

            file_name = f"Copom{number}-not{data}{number}.pdf"
            url = f"https://www.bcb.gov.br/content/copom/atascopom/{file_name}"

            print(f"🔗 Trying to download: {url}")
            response = requests.get(url)
            if response.status_code == 200:
                local_pdf_path = f"ata_copom_{number}.pdf"
                with open(local_pdf_path, "wb") as f:
                    f.write(response.content)
                print(f"📥 Success! Report {number} downloaded from: {url}")

                with open(history_file, "w") as f:
                    json.dump({"last_minute_read": number}, f)

                return self._extract_text_from_pdf(local_pdf_path)

        print("✅ No new minutes found. All available minutes have already been read.")
        return ""
    
    def _extract_text_from_pdf(self, path: str) -> str:
        text = ""
        with pdfplumber.open(path) as pdf:
            for page in pdf.pages:
                text += page.extract_text() + "\n"
        return text.strip()
