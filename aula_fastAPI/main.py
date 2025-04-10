from fastapi import FastAPI, HTTPException, status, Response, Depends
from typing import Optional, Any
from model import Pato

app = FastAPI(title="API Patos da ds 14", version="0.0.1", description="API que a sala escolheu")

def fake_db():
    try:
        print("conectatando no banco de dados")
    finally:
        print("fechando a conecção com o banco de dados")

patos = {
    1: {
        "nome": "Luca",
        "especie": "pato canadense",
        "idade": 25,
        "cor": "amarelo e verde",
        "foto": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTj_K1E3O-G4TnM52J30z819aF1k7yiPyswPA&s"
    },
    2: {
        "nome": "Perry",
        "especie": "ornitorrinco",
        "idade": 5,
        "cor": "verde com chapeu",
        "foto": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcROZoWmJJPwStTpLMgaaAcfaAgj8TDoldrWMw&s"
    }
}


@app.get("/", description="helo word", summary="Retorna nada")
async def raiz():
    return{"oiiiiiiiiiiii helo word né sou euuuu"}

@app.get("/patos", description="Retorna todos os patos quue tem no banco de dados", summary="Retorna todos os pstos")
async def get_patos(db: Any = Depends(fake_db)):
    return patos

@app.get("/patos/{pato_id}")
async def get_pato(pato_id: int):
    try:
        pato = patos[pato_id]
        return pato
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Não existe pato com o id {pato_id}")
    
@app.post("/patos", status_code=status.HTTP_201_CREATED)
async def post_pato(pato: Optional[Pato]= None):
    next_id = len(pato) + 1
    patos[next_id] = pato
    del pato.id 
    return pato

@app.put("/patos/{pato_id}", status_code=status.HTTP_202_ACCEPTED)
async def put_pato(pato_id: int, pato:Pato):
    if pato_id in pato:
        pato[pato_id] = pato
        pato.id = pato_id
        del pato.id
        return pato
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Não existe pato com o id {pato_id}")
    
@app.delete("/patos/{pato_id}")
async def delete_pato(pato_id: int):
    if pato_id in patos:
        del patos[pato_id]
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Não existe pato com o id {pato_id}")
    
@app.get("/caculadora")
async def calculadora(num1: int, num2:int):
    soma = num1 + num2
    return soma


if __name__ == "__main__":
    import uvicorn 
    uvicorn.run("main:app", host="127.0.0.1", port=8000, log_level="info", reload=True)