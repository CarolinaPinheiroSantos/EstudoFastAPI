from fastapi import FastAPI, HTTPException, status, Response, Depends
from typing import Optional, Any
from model import Cinema

app = FastAPI(title="API de Cinema", description="API programação dos filmes em cartaz no cinema")

cinema = {
    1: {
        "filme": "Avatar",
        "classificacao": 14,
        "genero": "aventura",
        "sobre": "No exuberante mundo alienígena de Pandora vivem os Na'vi, seres que parecem ser primitivos, mas são altamente evoluídos. Como o ambiente do planeta é tóxico, foram criados os avatares, corpos biológicos controlados pela mente humana que se movimentam livremente em Pandora",
        "capa": "https://upload.wikimedia.org/wikipedia/pt/b/b0/Avatar-Teaser-Poster.jpg",
        "data_horario": "05/10/2024 14:30:00"
    },
    2: {
        "filme": "Crepusculo",
        "classificacao": 16,
        "genero": "romance",
        "sobre": "A estudante Bella Swan conhece Edward Cullen, um belo mas misterioso adolescente. Edward é um vampiro, cuja família não bebe sangue, e Bella, longe de ficar assustada, se envolve em um romance perigoso com sua alma gêmea imortal.",
        "capa": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRUxE0ap_ktC_9N3lczwiSiOdd1BQ465xAXWQ&s",
        "data_horario": "29/03/2024 14:00:00"
    }
}

@app.get("/", description="Retorna todo filmes em cartaz do cinema")
async def todos_filme():
    return cinema

@app.get("/cinema/{filme_id}", description="Retorna a partir do id filme em cartaz do cinema")
async def cada_filme(filme_id:int):
    try:
        filme = cinema[filme_id]
        return filme
    except KeyError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Não existe nada em cartaz com o id {filme_id}")

@app.post("/cinema/criar", description="Cria filme em cartaz do cinema", status_code=status.HTTP_201_CREATED)
async def criar_filme(filme: Optional[Cinema]= None):
    increment_id = len(Cinema) + 1
    filme[increment_id] = filme
    del filme.id
    return filme

@app.put("/cinema/{filme_id}", description="Atualiza filme em cartaz do cinema", status_code=status.HTTP_202_ACCEPTED)
async def atualizar_filme(filme_id: int, filme:Cinema):
    if filme in cinema:
        filme[filme_id] = filme
        filme.id = filme_id
        del filme.id
        return filme
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Não existe filme com o id {filme_id}")
    
@app.delete("/cinema/{filme_id}")
async def delete_filme(filme_id: int):
    if filme_id in Cinema:
        del cinema[filme_id]
        return Response("apagouuuuuu", status_code=status.HTTP_204_NO_CONTENT)
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Não existe filme com o id {filme_id}")
    
