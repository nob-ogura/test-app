# 環境構築
1. terminal で実行したコマンド
```zsh
# システムの更新
sudo apt update
sudo apt upgrade -y

# 必要なパッケージのインストール
sudo apt install -y nginx python3 python3-pip nodejs npm

# Pythonの仮想環境作成
apt install python3.12-venv
python3.12 -m venv venv
source venv/bin/activate

# バックエンド用パッケージインストール
pip install fastapi uvicorn strawberry-graphql

# フロントエンド用セットアップ
npx create-react-app frontend
cd frontend
npm install @apollo/client graphql
```

2. nginx の設定
```
# /etc/nginx/sites-available/default
server {
    listen 80;
    server_name localhost;  # ローカル開発環境用

    # フロントエンド（静的ファイル）
    location / {
        root /var/www/html;  # Reactのビルドファイルを配置
        try_files $uri $uri/ /index.html;
    }

    # バックエンドAPI
    location /api {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }
}
```

3. systemd サービス設定
```
# /etc/systemd/system/fastapi.service
[Unit]
Description=FastAPI application
After=network.target

[Service]
User=ubuntu
WorkingDirectory=/home/n.ogura/test-app/backend
Environment="PATH=/home/n.ogura/test-app/venv/bin"
ExecStart=/home/n.ogura/test-app/venv/bin/uvicorn main:app --host 0.0.0.0 --port 8000

[Install]
WantedBy=multi-user.target
```

# バックエンド起動
1. cd ~/test-app/backend
2. source ~/venv/bin/activate
3. uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
4. acess to http://198.19.249.245:8000/graphql
