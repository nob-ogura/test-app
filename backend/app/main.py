# /home/n.ogura/test-app/backend/app/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import strawberry
from strawberry.fastapi import GraphQLRouter

# GraphQLの型定義
@strawberry.type
class Query:
    @strawberry.field
    def hello(self) -> str:
        return "Hello, World!"

# GraphQLスキーマの作成
schema = strawberry.Schema(query=Query)

# FastAPIアプリケーションの作成
app = FastAPI()

# CORSミドルウェアの設定（開発環境用）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# GraphQLルーターの設定
graphql_app = GraphQLRouter(schema)
app.include_router(graphql_app, prefix="/graphql")

# 必要に応じて追加のルートを定義
@app.get("/health")
async def health_check():
    return {"status": "healthy"}