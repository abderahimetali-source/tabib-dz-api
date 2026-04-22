from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="طبيب الجزائر API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

users_db = []
doctors_db = [
    {"id": 1, "name": "د. أحمد بن عمر", "specialty": "طب عام", "price": 2000, "wilaya": "الجزائر"},
    {"id": 2, "name": "د. فاطمة زهراء", "specialty": "طب أطفال", "price": 2500, "wilaya": "وهران"},
    {"id": 3, "name": "د. كريم منصوري", "specialty": "قلب", "price": 3000, "wilaya": "قسنطينة"}
]

class UserRegister(BaseModel):
    full_name: str
    email: str
    password: str
    phone: str

class LoginRequest(BaseModel):
    email: str
    password: str

@app.get("/")
def home():
    return {"message": "طبيب الجزائر API شغال 100%"}

@app.post("/register")
def register(user: UserRegister):
    for u in users_db:
        if u["email"] == user.email:
            raise HTTPException(status_code=400, detail="الإيميل مسجل")
    users_db.append(user.dict())
    return {"message": "تم التسجيل بنجاح"}

@app.post("/login")
def login(req: LoginRequest):
    for u in users_db:
        if u["email"] == req.email and u["password"] == req.password:
            return {"access_token": "token_123", "user": u["full_name"]}
    raise HTTPException(status_code=401, detail="الإيميل أو كلمة السر غلط")

@app.get("/doctors")
def get_doctors():
    return doctors_db
