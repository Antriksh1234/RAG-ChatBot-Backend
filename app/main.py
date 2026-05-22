import uuid
from fastapi import FastAPI
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from app.db import engine, SessionLocal
from app.models import Document, Base
from app.embeddings import generate_embedding
from app.schemas import DocumentCreate
from app.llm import generate_answer

from app.models import Document, DocumentChunk, Base
from app.utils import chunk_text

from app.schemas import DocumentCreate, SearchRequest
from sqlalchemy import select

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "RAG Chatbot Backend Running"}


@app.post("/documents")
def create_document(document: DocumentCreate):

    db: Session = SessionLocal()

    db_document = Document(
        title=document.title,
        content=document.content
    )

    db.add(db_document)

    db.commit()

    db.refresh(db_document)

    chunks = chunk_text(document.content)

    for index, chunk in enumerate(chunks):
        embedding = generate_embedding(chunk)

        db_chunk = DocumentChunk(
            document_id=db_document.id,
            chunk_index=index,
            chunk_text=chunk,
            embedding=embedding
        )

        db.add(db_chunk)

    db.commit()

    return {
        "id": str(db_document.id),
        "message": "Document created successfully",
        "chunks_created": len(chunks)
    }


@app.post("/search")
def semantic_search(request: SearchRequest):

    db: Session = SessionLocal()

    query_embedding = generate_embedding(request.query)

    results = db.query(DocumentChunk).order_by(
        DocumentChunk.embedding.cosine_distance(query_embedding)
    ).limit(5).all()

    return [
        {
            "chunk_index": result.chunk_index,
            "chunk_text": result.chunk_text
        }
        for result in results
    ]

@app.post("/chat")
def chat(request: SearchRequest):

    db: Session = SessionLocal()

    query_embedding = generate_embedding(request.query)

    results = db.query(
        DocumentChunk,
        DocumentChunk.embedding.cosine_distance(
            query_embedding
        ).label("distance")
    ).order_by("distance").limit(3).all()

    DISTANCE_THRESHOLD = 0.7

    best_distance = results[0].distance

    if best_distance > DISTANCE_THRESHOLD:
        return {
            "question": request.query,
            "answer": "I could not find relevant information in the uploaded documents.",
            "sources": []
        }

    context = "\n\n".join(
        [result.DocumentChunk.chunk_text for result in results]
    )

    llm_response = generate_answer(
        context=context,
        question=request.query
    )

    unique_sources = {}

    for result in results:

        doc_id = str(result.DocumentChunk.document.id)

        if doc_id not in unique_sources:

            unique_sources[doc_id] = {
                "document_id": doc_id,
                "document_title": result.DocumentChunk.document.title
            }

    return {
        "question": request.query,

        "answer": (
            llm_response["answer"]
            if llm_response["success"]
            else "LLM service is currently unavailable, but relevant documents were found."
        ),

        "sources": list(unique_sources.values())
    }

@app.get("/documents/{document_id}")
def get_document(document_id: str):

    db: Session = SessionLocal()

    document_uuid = uuid.UUID(document_id)

    document = db.query(Document).filter(
        Document.id == document_uuid
    ).first()

    if not document:
        return {
            "error": "Document not found"
        }

    return {
        "id": str(document.id),
        "title": document.title,
        "content": document.content,
        "created_at": document.created_at
    }