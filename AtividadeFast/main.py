from fastapi import FastAPI, Depends, Form, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import SessionLocal
from model import Cinema

app = FastAPI()

# Configurando o Jinja2 para usar a pasta "templates"
templates = Jinja2Templates(directory="templates")

# Middleware para fornecer sessões do banco para cada requisição
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Página inicial com formulário (GET)
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})

# Adicionar filme (POST)
@app.post("/adicionar", response_class=HTMLResponse)
def adicionar(
    request: Request,
    filme: str = Form(...),
    classificacao: int = Form(...),
    genero: str = Form(...),
    sobre: str = Form(...),
    capa: str = Form(...),
    data_horario: str = Form(...),
    db: Session = Depends(get_db)
):
    novo = Cinema(
        filme=filme,
        classificacao=classificacao,
        genero=genero,
        sobre=sobre,
        capa=capa,
        data_horario=data_horario
    )
    db.add(novo)
    db.commit()
    db.refresh(novo)
    return templates.TemplateResponse("home.html", {
        "request": request,
        "mensagem": f"Filme '{filme}' cadastrado com sucesso!"
    })

# Listar todos os filmes (GET)
@app.get("/listar", response_class=HTMLResponse)
def listar(request: Request, db: Session = Depends(get_db)):
    filmes = db.query(Cinema).all()
    return templates.TemplateResponse("listar.html", {
        "request": request,
        "filmes": filmes
    })
