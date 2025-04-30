from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional, Dict, Any, List
from datetime import datetime
import json
import os
import random

# Setează cheia API pentru modelul tău (OpenAI ca exemplu)
# openai.api_key = os.environ.get("OPENAI_API_KEY")

# Creează aplicația FastAPI
app = FastAPI(title="ChefMind API", description="API pentru chatbot-ul ChefMind - psiholog culinar")

# Configurare CORS pentru a permite accesul din frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Ajustează în funcție de adresa frontend-ului
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Model pentru mesajele primite
class MessageRequest(BaseModel):
    text: str
    sender: str
    timestamp: Optional[str] = None

# Model pentru răspunsurile bot-ului
class MessageResponse(BaseModel):
    text: str
    timestamp: str

# Bază de cunoștințe simplă pentru rețete și sfaturi bazate pe stări emoționale
FOOD_MOOD_KNOWLEDGE = {
    "fericit": [
        "Energiile tale pozitive pot fi amplificate cu alimente bogate în antioxidanți precum fructele de pădure.",
        "Celebrează starea ta bună cu o rețetă de salată colorată cu quinoa, avocado și portocale.",
        "Bucuria ta poate fi susținută cu omega-3 din pește și nuci, care ajută la menținerea sănătății creierului."
    ],
    "trist": [
        "Când ești trist, creierul tău ar putea beneficia de alimente bogate în triptofan precum curcanul, ouăle sau semințele de dovleac.",
        "Încearcă o supă caldă cu legume și ghimbir pentru a-ți ridica starea de spirit.",
        "Ciocolata neagră (peste 70% cacao) poate stimula producția de endorfine - hormoni ai fericirii."
    ],
    "stresat": [
        "Alimentele bogate în magneziu precum spanacul și nucile pot ajuta la reducerea anxietății.",
        "Un ceai de mușețel sau lavandă poate avea efect calmant asupra sistemului nervos.",
        "Evită cafeina și zahărul, care pot amplifica sentimentele de stres și neliniște."
    ],
    "obosit": [
        "Proteinele slabe și carbohidrații complecși îți pot oferi energie de lungă durată.",
        "Smoothie-urile cu spanac, banană și semințe de chia pot fi o sursă excelentă de nutrienți care combat oboseala.",
        "Asigură-te că ești hidratat - deshidratarea este o cauză frecventă a oboselii."
    ],
    "poftă_dulce": [
        "Fructele coapte pot satisface pofta de dulce într-un mod sănătos.",
        "Încearcă un desert de avocado cu cacao și miere pentru o alternativă nutritivă la dulciurile procesate.",
        "Iaurtul grecesc cu miere și fructe poate satisface pofta de dulce oferind și proteine benefice."
    ],
    "poftă_sărat": [
        "Încearcă chipsuri de kale coapte cu puțină sare de mare pentru o alternativă sănătoasă.",
        "Popcornul făcut acasă cu condimente poate satisface pofta de sărat cu mai puțin sodiu.",
        "Nucile și semințele prăjite ușor cu condimente pot fi o gustare sățioasă și sănătoasă."
    ]
}

# Exemple de rețete pentru diferite stări emoționale
RECIPES = {
    "fericit": [
        {
            "nume": "Bowl de energie cu quinoa și fructe",
            "ingrediente": ["1 cană quinoa", "2 căni apă", "1 cană fructe de pădure mixte", "1 banană", "2 linguri miere", "Semințe de chia"],
            "preparare": "Fierbe quinoa în apă timp de 15 minute. Lasă să se răcească. Amestecă cu fructele tăiate, miere și presară semințe de chia deasupra."
        }
    ],
    "trist": [
        {
            "nume": "Supă reconfortantă de legume",
            "ingrediente": ["1 ceapă", "2 morcovi", "1 cartof dulce", "1 lingură ghimbir ras", "1 litru supă de legume", "Sare și piper"],
            "preparare": "Sotează ceapa, adaugă legumele tăiate cubulețe și ghimbirul. Adaugă supa și fierbe până legumele sunt moi. Pasează totul pentru o textură cremoasă."
        }
    ],
    "stresat": [
        {
            "nume": "Smoothie anti-stres",
            "ingrediente": ["1 banană", "1 cană spanac", "1/2 avocado", "1 lingură pudră de cacao", "1 cană lapte de migdale", "1 lingură miere"],
            "preparare": "Amestecă toate ingredientele într-un blender până obții o textură fină. Servește imediat."
        }
    ]
}

# Răspunsuri generale pentru întrebări comune
GENERAL_RESPONSES = [
    "Ca psiholog culinar, îți pot recomanda alimente care nu doar că au gust bun, dar îți pot și îmbunătăți starea de spirit.",
    "Alimentația și starea emoțională sunt strâns legate. Ce mâncăm poate influența semnificativ cum ne simțim.",
    "Există alimente care pot reduce stresul, combate depresia și îmbunătăți concentrarea. Aș putea să-ți recomand câteva bazate pe nevoile tale.",
    "Tehnicile de mindful eating te pot ajuta să te bucuri mai mult de mâncare și să dezvolți o relație mai sănătoasă cu alimentele."
]

# Funcție pentru a identifica emoția sau preferința alimentară din mesaj
def identify_emotion_or_food_preference(text: str) -> List[str]:
    text = text.lower()
    
    emotions = []
    
    # Identifică emoții din text
    if any(word in text for word in ["fericit", "bucurie", "bucuros", "vesel", "bine"]):
        emotions.append("fericit")
    
    if any(word in text for word in ["trist", "supărat", "deprimat", "depresie", "melancolie"]):
        emotions.append("trist")
    
    if any(word in text for word in ["stresat", "anxios", "anxietate", "stres", "nervos", "tensionat"]):
        emotions.append("stresat")
    
    if any(word in text for word in ["obosit", "epuizat", "lipsit de energie", "fără putere"]):
        emotions.append("obosit")
    
    # Identifică preferințe alimentare
    if any(word in text for word in ["dulce", "ciocolată", "desert", "prăjitură", "zahăr"]):
        emotions.append("poftă_dulce")
    
    if any(word in text for word in ["sărat", "chips", "crocant", "sărate"]):
        emotions.append("poftă_sărat")
    
    return emotions if emotions else ["general"]

# Funcție pentru a genera răspunsuri personalizate
def generate_response(message: str) -> str:
    # Identifică starea emoțională sau preferința alimentară
    categories = identify_emotion_or_food_preference(message)
    
    response_parts = []
    
    # Adaugă un răspuns general dacă nu avem o categorie specifică
    if "general" in categories:
        response_parts.append(random.choice(GENERAL_RESPONSES))
        response_parts.append("Poți să-mi spui cum te simți sau ce poftă ai, și îți pot oferi recomandări personalizate.")
        return " ".join(response_parts)
    
    # Adaugă sfaturi nutriționale bazate pe emoții/preferințe
    for category in categories:
        if category in FOOD_MOOD_KNOWLEDGE:
            response_parts.append(random.choice(FOOD_MOOD_KNOWLEDGE[category]))
    
    # Adaugă o rețetă dacă avem disponibilă pentru categoria identificată
    recipe_categories = [cat for cat in categories if cat in RECIPES]
    if recipe_categories:
        category = random.choice(recipe_categories)
        recipe = random.choice(RECIPES[category])
        response_parts.append(f"\n\nIată o rețetă care ți-ar putea plăcea: **{recipe['nume']}**")
        response_parts.append("\nIngrediente:")
        response_parts.append(", ".join(recipe['ingrediente']))
        response_parts.append("\nPreparare:")
        response_parts.append(recipe['preparare'])
    
    # Adaugă o invitație la final
    response_parts.append("\n\nAi vreo întrebare specifică despre această recomandare sau despre cum te poate ajuta alimentația să-ți îmbunătățești starea?")
    
    return " ".join(response_parts)

# Ruta pentru procesarea mesajelor
@app.post("/api/process-message", response_model=MessageResponse)
async def process_message(message: MessageRequest):
    if not message.text:
        raise HTTPException(status_code=400, detail="Mesajul nu poate fi gol")
    
    # Generează răspunsul
    response_text = generate_response(message.text)
    
    # Pentru un sistem mai avansat, s-ar putea folosi un model de AI (OpenAI, Hugging Face, etc.)
    # response = openai.ChatCompletion.create(
    #     model="gpt-3.5-turbo",
    #     messages=[
    #         {"role": "system", "content": "Ești ChefMind, un psiholog culinar care oferă sfaturi despre alimentație și stare emoțională."},
    #         {"role": "user", "content": message.text}
    #     ]
    # )
    # response_text = response.choices[0].message["content"]
    
    # Returnează răspunsul formatat
    return MessageResponse(
        text=response_text,
        timestamp=datetime.now().isoformat()
    )

# Ruta de bază pentru verificarea stării API-ului
@app.get("/")
async def root():
    return {"message": "ChefMind API funcționează", "status": "online"}

# Rulează aplicația cu uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)