from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, init_db, Operation
from models import OperationRequest, OperationResponse
from operations import compute_pow, compute_fact, compute_fib
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Math Microservice")



app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


init_db()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/compute", response_model=OperationResponse)
def compute(op: OperationRequest, db: Session = Depends(get_db)):
    if op.type == "pow":
        result = compute_pow(op.x, op.y)
    elif op.type == "fact":
        result = compute_fact(op.x)
    elif op.type == "fib":
        result = compute_fib(op.x)
    else:
        raise HTTPException(status_code=400, detail="Invalid operation type")

    # Persist to DB
    record = Operation(type=op.type, x=op.x, y=op.y, result=str(result))
    db.add(record)
    db.commit()
    db.refresh(record)

    return {"result": result}
