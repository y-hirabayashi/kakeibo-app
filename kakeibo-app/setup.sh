#!/bin/bash
set -e

echo "✅ システム更新"
sudo apt update
sudo apt upgrade -y

echo "✅ 必要パッケージ"
sudo apt install -y python3-venv python3-pip python3-dev git

echo "✅ venv作成"
python3 -m venv ~/kakeibo_venv
source ~/kakeibo_venv/bin/activate

echo "✅ pip更新"
pip install --upgrade pip setuptools wheel

echo "✅ ansibleインストール"
pip install ansible

echo "✅ プロジェクト取得"
if [ ! -d ~/kakeibo-app ]; then
  git clone https://github.com/y-hirabayashi/kakeibo-app.git ~/kakeibo-app
fi

echo "✅ ansible playbook 実行"
cd ~/kakeibo-app
ansible-playbook playbook.yml

echo "🎉 セットアップ完了"
