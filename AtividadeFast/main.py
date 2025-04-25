from fastapi import FastAPI, Depends, Form, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from database import SessionLocal
from model import Cinema

app = FastAPI(title="API de Cinema", description="API programação dos filmes em cartaz no cinema")

templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("home.html", {"request": request})


@app.get("/listar", response_class=HTMLResponse)
def listar(request: Request, db: Session = Depends(get_db)):
    filmes = db.query(Cinema).all()
    return templates.TemplateResponse("listar.html", {
        "request": request,
        "filmes": filmes
    })

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
        "request": request
    })

@app.delete("/excluir/{filme_id}")
def excluir(filme_id: int, db: Session = Depends(get_db)):
    filme = db.query(Cinema).filter(Cinema.id == filme_id).first()
    if not filme:
        raise HTTPException(status_code=404, detail="Filme não encontrado")
    db.delete(filme)
    db.commit()
    return RedirectResponse(url="/listar", status_code=303)


@app.get("/editar/{filme_id}", response_class=HTMLResponse)
def editar(filme_id: int, request: Request, db: Session = Depends(get_db)):
    filme = db.query(Cinema).filter(Cinema.id == filme_id).first()
    if not filme:
        raise HTTPException(status_code=404, detail="Filme não encontrado")
    return templates.TemplateResponse("editar.html", {
        "request": request,
        "filme": filme
    })

@app.post("/atualizar/{filme_id}")
def atualizar(filme_id: int, filme: str = Form(...), classificacao: int = Form(...), genero: str = Form(...), 
              sobre: str = Form(...), capa: str = Form(...), data_horario: str = Form(...), db: Session = Depends(get_db)):
    filme_db = db.query(Cinema).filter(Cinema.id == filme_id).first()
    if not filme_db:
        raise HTTPException(status_code=404, detail="Filme não encontrado")

    filme_db.filme = filme
    filme_db.classificacao = classificacao
    filme_db.genero = genero
    filme_db.sobre = sobre
    filme_db.capa = capa
    filme_db.data_horario = data_horario

    db.commit()
    db.refresh(filme_db)

    return RedirectResponse(url="/listar", status_code=303)
