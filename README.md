# kakeibo-app 環境構築手順
- ユーザー名は「ubuntu」で環境構築してください
- パスは適宜変更してください
- inventory.iniのリモート台数、秘密鍵のパス、IPは適宜変更してください


## 📦 セットアップ手順
以下の手順で環境構築を行ってください
**VirtualBox(EC2) で Ubuntu** を起動（EC2の場合はSSH接続）
**GitHub からソース取得**
**仮想環境アクティベート**

**docker compose 起動確認**
```basu
sudo docker compose ps
# sudo usermod -aG docker ubuntu
# newgrp docker
```

# 🧾 Kakeibo App

Flask × Docker × Ansible 構成のミニマル家計簿アプリケーションです。支出・収入の記録、CSV出力、月別・カテゴリ別サマリ表示が可能です。

---

## 🚀 クイックスタート

### 🔧 前提
- Python 3.12+
- Docker & Docker Compose
- Ansible

### ⬇️ セットアップ（ローカル環境）

```bash
sudo apt update && sudo apt install git -y
git clone https://github.com/y-hirabayashi/kakeibo-app.git
cd kakeibo-app
# sudo chmod +x setup.sh
./setup.sh
source ~/kakeibo_venv/bin/activate

# Ansibleでローカル環境構築
ansible-playbook -i inventory.ini -l local playbook.yml

# ブラウザでアクセス
http://localhost:5000
🐳 Docker コンテナ構成
サービス	内容	ポート
web	Flaskアプリ	5000
db_data	SQLite 永続化	ホスト共有

📂 ディレクトリ構成
```bash
kakeibo-app/
├── app/                # Flask アプリ本体
├── db_data/            # SQLite データ保存（マウント）
├── templates/          # HTML テンプレート
├── docker-compose.yml
├── playbook.yml        # Ansible構成
└── README.md
```
⚙️ Ansibleの使い方
```bash
# ローカル実行
ansible-playbook -i inventory.ini -l local playbook.yml

# リモート実行
ansible-playbook -i inventory.ini -l remote playbook.yml
```
📈 機能一覧
支出・収入の登録、編集、削除
月別サマリ表示（収支グラフ）
カテゴリ別サマリ
CSVエクスポート（UTF-8 BOM付でExcel対応）

🔧 今後の改善予定
OSS DB（PostgreSQL/MySQL）への切替
認証機能（ログイン）
CI/CD（GitHub Actions）
テスト追加（pytest）

📝 ライセンス
MIT License

📬 開発者
y-hirabayashi
GitHub: y-hirabayashi

```yaml
この内容をそのまま `README.md` に貼り付けて問題ありません。必要ならこれをコミットしてプッシュするコマンドもご案内できます。
```
