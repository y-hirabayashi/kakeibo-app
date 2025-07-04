#!/bin/bash
set -e

echo "✅ システム更新"
sudo apt update
sudo apt upgrade -y

echo "✅ 必要パッケージ"
sudo apt install -y python3-venv python3-pip python3-dev git

echo "✅ venv 作成"
python3 -m venv ~/kakeibo_venv
source ~/kakeibo_venv/bin/activate

echo "✅ pip 更新"
pip install --upgrade pip setuptools wheel

echo "✅ ansible インストール"
pip install ansible

echo "✅ ansible playbook 実行"
ansible-playbook playbook.yml

echo "🎉 セットアップ完了"
