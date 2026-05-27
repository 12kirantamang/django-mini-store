# 🛒 Django ミニストア

> Djangoで構築したシンプルかつ実用的なeコマースWebアプリケーションです。小規模なオンライン小売業向けに設計されています。

![Django](https://img.shields.io/badge/Django-4.x-green)
![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Stripe](https://img.shields.io/badge/Stripe-Payments-blue)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## 📌 概要

**Django ミニストア**は、ユーザーが商品を閲覧し、ショッピングカートを管理し、ウィッシュリストに保存し、Stripeによる本番決済で注文できる軽量なeコマースプラットフォームです。CSV出力機能を備えた管理パネルも搭載しています。

### 対象ユーザー
- シンプルな購買体験を求めるオンラインショッパー
- 基本的な店舗管理システムを必要とする中小企業オーナー
- DjangoのeコマースパターンをいちからDjangoを学ぶ開発者

---

## 🌐 デモ

**ローカルデモ：** `http://localhost:8000/`

| ホームページ | 商品一覧 | カートページ | 管理パネル |
|-----------|-------------|-----------|-------------|
| ![Home](https://github.com/user-attachments/assets/bf90586c-2fee-4950-b06a-e22d31486b70) | ![Product List](https://github.com/user-attachments/assets/c25f8ec8-8904-49a3-bd56-5d32f96c6111) | ![Cart](https://github.com/user-attachments/assets/63826cae-0d9c-470d-90ba-d4e7ef63bc44) | ![Admin Panel](https://github.com/user-attachments/assets/bca5a818-7384-4e63-a71b-9795fe1497bc) |

---

## 🚀 機能一覧

### 👤 ユーザー向け機能

| 機能 | 説明 |
|------|------|
| **ユーザー登録・ログイン** | 安全なアカウント作成と認証 |
| **商品閲覧・検索** | 詳細ページ付きの商品一覧と検索 |
| **ウィッシュリスト** | 気に入った商品をあとで買うために保存 |
| **カートに追加** | 商品の選択と数量管理 |
| **カート管理** | 数量の更新・商品の削除 |
| **注文確定** | チェックアウトの完了 |
| **Stripe決済** | Stripeチェックアウトによる安全なカード決済 |

### 🔧 管理者向け機能

| 機能 | 説明 |
|------|------|
| **商品管理** | 商品のCRUD操作（作成・閲覧・更新・削除） |
| **ユーザー管理** | 登録ユーザーの閲覧と管理 |
| **注文管理** | 顧客注文の追跡と処理 |
| **CSVエクスポート** | 注文・商品データのCSVファイル出力 |

---

## 🛠️ 技術スタック

| カテゴリ | 技術 |
|---------|------|
| **バックエンド** | Python 3.9+、Django 4.x |
| **データベース** | SQLite（開発環境）/ MySQL（本番環境） |
| **フロントエンド** | HTML、CSS、JavaScript |
| **認証** | Django 組み込み認証 |
| **決済** | Stripe（stripe-python SDK） |
| **エクスポート** | Python 標準 `csv` モジュール |

---

## 🗄️ データベース設計（ER図）

![ER図](https://github.com/user-attachments/assets/fd4f25dc-e810-4d24-9229-cded9b396f13)

### エンティティ関係

- **ユーザー** → **カート**（1対多）
- **ユーザー** → **注文**（1対多）
- **ユーザー** → **ウィッシュリスト**（1対1）
- **ウィッシュリスト** → **商品**（多対多）
- **注文** → **注文明細**（1対多）
- **商品** → **注文明細**（1対多）
- **商品** → **カート**（1対多）

---

## 🏗️ インフラ構成図

![インフラ構成図](https://github.com/user-attachments/assets/b12569d2-248d-460a-9270-5ad4aabf2bd6)

### アーキテクチャ概要

| レイヤー | 技術 | 役割 |
|---------|------|------|
| クライアント | Webブラウザ | ユーザーインターフェース |
| Webサーバー | Nginx + Gunicorn | リバースプロキシ・SSL・静的ファイル配信 |
| アプリケーション | Django | ビジネスロジック・テンプレート・管理画面 |
| データベース | SQLite / MySQL / PostgreSQL | データ永続化 |
| 決済 | Stripe API | 安全な決済処理 |

### リクエストフロー

1. **クライアント**がHTTPSリクエストを送信
2. **Nginx**がSSLを処理しGunicornにルーティング
3. **Gunicorn**がWSGIリクエストをDjangoに渡す
4. **Django**がロジックを処理しORMでデータベースに問い合わせ
5. チェックアウト時：**Django**がStripeセッションを作成しユーザーをリダイレクト
6. **Stripe**が決済を処理しWebhookで確認を送信
7. **データベース**がデータを返し、レスポンスをクライアントに返却

---

## 💳 Stripe決済連携

本プロジェクトは安全な決済処理に [Stripe Checkout](https://stripe.com/docs/payments/checkout) を使用しています。

### 仕組み

1. ユーザーがカートページから **「チェックアウトへ進む」** をクリック
2. DjangoがカートアイテムをもとにStripeの `checkout.Session` を作成
3. ユーザーがStripeのホスト型チェックアウトページにリダイレクト
4. 決済完了後、Stripeが `/payments/webhook/` にWebhookイベントを送信
5. Djangoが決済を確認し注文を作成

### Stripeのセットアップ

```bash
# Stripe SDKのインストール
pip install stripe

# .envファイルに追記
STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...
```

> ⚠️ **Stripeのシークレットキーは絶対にコミットしないでください。** 必ず環境変数で管理してください。

### テスト決済（テストモード）

[Stripeのテストカード番号](https://stripe.com/docs/testing) を使用してください：

| カード番号 | シナリオ |
|-----------|---------|
| `4242 4242 4242 4242` | 決済成功 |
| `4000 0000 0000 0002` | カード拒否 |
| `4000 0025 0000 3155` | 認証が必要（3Dセキュア） |

有効期限は未来の日付、CVCは任意の3桁を入力してください。

---

## ❤️ ウィッシュリスト

ユーザーは気に入った商品をウィッシュリストに保存し、あとで購入することができます。

### 機能

- 商品のウィッシュリストへの追加・削除
- 専用ページでウィッシュリスト内の商品を一覧表示
- ウィッシュリストからカートへ直接移動

### 仕組み

- 各ユーザーは `Wishlist` を1つ持ちます（初回使用時に自動作成）
- ウィッシュリストは `Product` との `ManyToManyField` で商品を管理
- ログイン済みユーザーのみ利用可能 — 未ログインの場合はログインページにリダイレクト

---

## 📥 CSVエクスポート

管理者はDjango管理パネルから直接、店舗データをCSVファイルとしてエクスポートできます。

### エクスポート対象

| エクスポート | 含まれるフィールド |
|------------|----------------|
| **注文** | 注文ID・ユーザー・日付・ステータス・合計金額 |
| **注文明細** | 注文ID・商品名・数量・単価 |
| **商品** | ID・名前・カテゴリ・価格・在庫・作成日 |

### エクスポートの手順

1. **Django管理画面** → エクスポートしたいモデル（例：注文）を選択
2. エクスポートするレコードを選択（または全件選択）
3. アクションのドロップダウンから **「選択したものをCSVでエクスポート」** を選択
4. **実行** をクリック — ファイルがすぐにダウンロードされます

### 実装について

CSVエクスポートアクションは `admin.py` でDjangoのアクションAPIとPython標準の `csv` モジュールを使って実装されており、追加の依存ライブラリは不要です。

---

## 📦 インストール手順

### 必要な環境

- Python 3.9+
- pip
- Git
- [Stripeアカウント](https://dashboard.stripe.com/register)（テストは無料）

### セットアップ手順

```bash
# 1. リポジトリのクローン
git clone https://github.com/12kirantamang/django-mini-store.git
cd django-mini-store

# 2. 仮想環境の作成
python -m venv venv

# 3. 仮想環境の有効化
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# 4. 依存パッケージのインストール
pip install -r requirements.txt

# 5. 環境変数の設定
cp .env.example .env
# .envファイルにSECRET_KEYとStripeキーを記入

# 6. マイグレーションの実行
python manage.py migrate

# 7. スーパーユーザー（管理者）の作成
python manage.py createsuperuser

# 8. 開発サーバーの起動
python manage.py runserver

# 9. アプリケーションへのアクセス
# ユーザーサイト：  http://localhost:8000/
# 管理パネル：      http://localhost:8000/admin/
```

### 環境変数（`.env`）

```env
SECRET_KEY=your-django-secret-key
DEBUG=True

STRIPE_PUBLIC_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# オプション：本番環境用
DATABASE_URL=mysql://user:password@host/dbname
```

---

## 🗂️ プロジェクト構成

```
django-mini-store/
├── accounts/          # ユーザー登録・ログイン・プロフィール
├── products/          # 商品一覧・詳細・検索
├── cart/              # カートのロジックとセッション管理
├── orders/            # 注文の確定と履歴
├── wishlist/          # ウィッシュリストの追加・削除・表示
├── payments/          # Stripeチェックアウトとwebhookハンドラー
├── config/            # Django設定・URL・WSGI
├── templates/         # HTMLテンプレート
├── static/            # CSS・JS・画像
├── media/             # ユーザーがアップロードした商品画像
├── manage.py
├── requirements.txt
└── .env.example
```

---

## 🔒 セキュリティに関する注意

- `SECRET_KEY` およびStripeキーは環境変数で管理し、ハードコーディングしません
- Stripe Webhookの署名はすべての受信イベントで検証されます
- カート・ウィッシュリスト・注文のすべてのビューは `@login_required` が必要です
- DjangoのCSRF保護がすべてのフォームで有効になっています

---

## 🤝 コントリビューション

プルリクエスト歓迎です。大きな変更を行う場合は、まずIssueを作成して内容を相談してください。

---

## 📄 ライセンス

このプロジェクトは [MITライセンス](LICENSE) のもとで公開されています。
