from openai import OpenAI
from pydantic import BaseModel, ConfigDict
import json

client = OpenAI(api_key="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")

class AnswersModel(BaseModel):
    model_config = ConfigDict(extra="forbid")

    skad_pochodzisz: list[str]
    kim_jestes: list[str]
    misja: list[str]
    sprzymierzeniec: list[str]
    cecha: list[str]
    bron: list[str]
    umiejetnosc: list[str]
    slabosc: list[str]
    zagrozenie: list[str]
    tajemnica: list[str]

def create_prompt(univers):
    return (
    f"Jesteś twórcą wideo w stylu 'Spin the wheel'. Odpowiadasz na poniższe pytania, korzystając wyłącznie z uniwersum {univers}."
    "Odpowiadaj tylko w formacie JSON, bez żadnych wyjaśnień, opisów czy dodatkowych komentarzy."
    "Każda odpowiedź musi być listą 10 krótkich nazw, posortowanych rosnąco według jakości: od najgorszej (1/10) do najlepszej (10/10). Pierwsza pozycja to najgorsza możliwa odpowiedź, ostatnia to najlepsza możliwa odpowiedź."
    "Struktura odpowiedzi:"
    "{"
    "1. Skąd pochodzisz: [najgorsza, ..., najlepsza],"
    "2. Kim jesteś: [najgorsza, ..., najlepsza],"
    "3. Jaka jest twoja misja: [najgorsza, ..., najlepsza],"
    "4. Kogo masz za sprzymierzeńca: [najgorsza, ..., najlepsza],"
    "5. Twoja najbardziej charakterystyczna cecha: [najgorsza, ..., najlepsza],"
    "6. Jaką masz broń: [najgorsza, ..., najlepsza],"
    "7. Jaką specjalną umiejętność posiadasz: [najgorsza, ..., najlepsza],"
    "8. Twoja największa słabość: [najgorsza, ..., najlepsza],"
    "9. Co ci zagraża: [najgorsza, ..., najlepsza],"
    "10. Jaką tajemnicę skrywasz przed innymi: [najgorsza, ..., najlepsza]"
    "}"
    "Przykład sortowania (dla pytania o broń): ['Patyk', 'Stary kij', ..., 'Miecz światła']"
    "Pamiętaj: Liczy się tylko poprawna kolejność od najgorszej do najlepszej. Odpowiadaj tylko w JSON, bez wyjaśnień, odpowiedzi podaj w języku angielskim"
)

def get_ai_request(system_prompt):
    response = client.beta.chat.completions.parse(
    model="gpt-4.1-nano",
    messages=[
        {"role": "system", "content": system_prompt},
    ],
    response_format=AnswersModel
    )
    content = json.loads(response.choices[0].message.content)
    answers = AnswersModel(**content)
    return answers

