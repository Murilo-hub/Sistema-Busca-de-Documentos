from __future__ import annotations
"""
app/schemas/document.py
──────────────────────────────────────────────────────────────────────────────
Schemas Pydantic para documentos.
 
  DocumentMetadata      → campos preenchidos pelo usuário no upload
  DocumentResponse      → dados retornados pela API após upload/listagem
  DocumentListResponse  → resposta paginada da listagem
──────────────────────────────────────────────────────────────────────────────
"""
 
from datetime import datetime
from pydantic import BaseModel, Field, computed_field   # computed_field importado corretamente
 
 
# ── Metadados enviados pelo usuário no upload ─────────────────────────────────
class DocumentMetadata(BaseModel):
    empresa:        str       = Field(..., min_length=1, max_length=200)   # obrigatório
    categoria:      str       = Field(..., min_length=1, max_length=100)   # obrigatório
    data_documento: str | None = None   # formato livre: "2024-01-15"
    descricao:      str | None = None   # descrição opcional
 
 
# ── Dados de um documento retornados pela API ─────────────────────────────────
class DocumentResponse(BaseModel):
    id:             int
    filename:       str           # nome gerado (uuid.ext)
    original_name:  str           # nome original do arquivo
    file_size:      int           # tamanho em bytes
    file_type:      str           # extensão: pdf, docx, txt...
    empresa:        str
    categoria:      str
    data_documento: str | None
    descricao:      str | None
    status:         str           # pending | processing | indexed | error
    chunks_count:   int           # quantos chunks foram gerados na indexação
    created_at:     datetime
    indexed_at:     datetime | None
 
    # computed_field DEVE estar dentro da classe — o bug anterior era tê-lo fora
    @computed_field                          # type: ignore[misc]
    @property
    def file_size_readable(self) -> str:
        """Converte bytes para leitura humana: KB ou MB."""
        if self.file_size < 1024 * 1024:
            return f"{self.file_size / 1024:.1f} KB"
        return f"{self.file_size / (1024 * 1024):.1f} MB"
 
    # from_attributes=True permite criar o schema a partir de um model SQLAlchemy
    model_config = {"from_attributes": True}
 
 
# ── Resposta paginada da listagem de documentos ───────────────────────────────
class DocumentListResponse(BaseModel):
    items:  list[DocumentResponse]   # documentos da página atual
    total:  int                      # total de documentos do usuário
    page:   int = 1                  # página atual (começa em 1)
    limit:  int = 20                 # itens por página
 
