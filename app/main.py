import uuid
from fastapi import FastAPI
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware

from app.db import engine, SessionLocal
from app.embeddings import generate_embedding
from app.schemas import DocumentCreate, SearchRequest, DocumentUpdate
from app.llm import generate_answer

from app.models import Document, DocumentChunk, Base
from app.utils import chunk_text

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def create_document_chunks(
    db: Session,
    document: Document
):

    chunks = chunk_text(document.content)

    for index, chunk in enumerate(chunks):

        embedding = generate_embedding(chunk)

        document_chunk = DocumentChunk(
            document_id=document.id,
            chunk_index=index,
            chunk_text=chunk,
            embedding=embedding
        )

        db.add(document_chunk)

    db.commit()

    return len(chunks)


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

    length = create_document_chunks(
        db=db,
        document=db_document
    )

    return {
        "id": str(db_document.id),
        "message": "Document created successfully",
        "chunks_created": length
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
    ).order_by("distance").limit(5).all()

    DISTANCE_THRESHOLD = 0.7

    filtered_results = [
        result
        for result in results
        if result.distance < DISTANCE_THRESHOLD
    ]

    print("\n--- RETRIEVAL RESULTS ---")

    for result in filtered_results:

        print(
            f"""
Document: {result.DocumentChunk.document.title}

Distance: {result.distance}

Chunk Preview:
{result.DocumentChunk.chunk_text[:200]}
"""
        )

    print("--- END RETRIEVAL RESULTS ---\n")

    if not filtered_results:

        return {
            "question": request.query,
            "answer": "I could not find relevant information in the uploaded documents.",
            "sources": []
        }

    context = "\n\n".join(
        [
            result.DocumentChunk.chunk_text
            for result in filtered_results
        ]
    )

    llm_response = generate_answer(
        context=context,
        question=request.query
    )

    unique_sources = {}

    for result in filtered_results:

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

@app.get("/documents")
def get_documents():

    db: Session = SessionLocal()

    documents = db.query(Document).order_by(
        Document.created_at.desc()
    ).all()

    return [
        {
            "id": str(document.id),
            "title": document.title,
            "created_at": document.created_at
        }
        for document in documents
    ]


@app.put("/documents/{document_id}")
def update_document(
    document_id: str,
    updated_document: DocumentUpdate
):

    db: Session = SessionLocal()

    document_uuid = uuid.UUID(document_id)

    document = db.query(Document).filter(
        Document.id == document_uuid
    ).first()

    if not document:
        return {
            "error": "Document not found"
        }

    document.title = updated_document.title
    document.content = updated_document.content

    db.commit()

    db.query(DocumentChunk).filter(
        DocumentChunk.document_id == document.id
    ).delete()

    db.commit()

    chunks_created = create_document_chunks(
        db=db,
        document=document
    )

    return {
        "message": "Document updated successfully",
        "document_id": str(document.id),
        "chunks_created": chunks_created
    }