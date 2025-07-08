# kakeibo-app 環境構築手順
ユーザー名は「ubuntu」で環境構築してください

## 🖥 対象環境

- Ubuntu 22.04（VirtualBox など）
- Python 3.12
- git
- ansible
- docker

## 📦 セットアップ手順
以下の手順で環境構築を行ってください

**VirtualBox(EC2) で Ubuntu** を起動（EC2の場合はSSH接続）

**GitHub からソース取得**

```bash
sudp apt update
sudo apt install git
git clone https://github.com/y-hirabayashi/kakeibo-app.git
```

**作業ディレクトリ、パーミッションの変更、スクリプト実行**

```bash
cd kakeibo-app
sudo chmod +x setup.sh
./setup.sh
```

**仮想環境アクティベート**

```bash
source ~/kakeibo_venv/bin/activate
```
**ansible実行、ホスト(ローカル)**
```bash
ansible-playbook -i inventory.ini -l local playbook.yml
```
**ansible実行、リモートサーバ**
```bash
ansible-playbook -i inventory.ini -l remote playbook.yml
```

**docker compose 起動確認**

```basu
sudo docker compose ps
#sudo usermod -aG docker ubuntu
#newgrp docker
```
