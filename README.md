## Quantum Circuit Demo API (Django + Qiskit)

<img src="https://img.shields.io/badge/-Django-092E20.svg?logo=django&style=flat">
<img src="https://img.shields.io/badge/-Qiskit-00ffaa.svg">

Djangoの単一エンドポイントAPI。フロントエンドで配置されたゲート・制御点の座標情報を受け取り、4量子ビットの量子回路（Qiskit）を構築、状態ベクトルから確率分布を計算して返す。

### エンドポイント

`POST /execute_python_code/`

リクエストボディ:

```json
{
  "img_data": [["H", 230, 150], ["CXA", 350, 260]],
  "dot_data": [["CXAD", 1]]
}
```

- `img_data`: `[ゲート名, x座標, y座標]` の配列。
  座標は6列(`i=0..5`)×4行(`j=0..3`)のグリッドセル（セル中心 `x=230+120*i`, `y=150+110*j`、許容幅±30）に対応し、`j` がそのままターゲット量子ビット番号（0〜3）になる。
  ゲート名の部分文字列で判定する:
  - `"CC"` を含み `"X"` を含む → トフォリゲート（`qc.ccx`）
  - `"C"` を含み `"H"`/`"X"`/`"Z"` を含む（`"CC"` でない）→ 制御ゲート（`qc.ch`/`qc.cx`/`qc.cz`）
  - それ以外で `"X"`/`"H"`/`"Z"`/`"Y"` を含む → 単一量子ビットゲート
- `dot_data`: 制御点情報 `[キー, 制御量子ビット番号, ...]`。
  - 単一制御ゲートは `dot_info[0] == ゲート名 + "D"` の行から制御量子ビット（`dot_info[1]`）を取得。
  - トフォリゲートは `dot_info[0] == ゲート名 + "D_1"` から1つ目の制御（`dot_info[2]`）、`dot_info[1] == ゲート名 + "D_2"` から2つ目の制御（`dot_info[3]`）を取得。

レスポンス:

```json
{
  "result": {
    "0000": 0.5,
    "0001": 0.5
  }
}
```

`Statevector.probabilities_dict()` の結果（基底状態のビット列 → 確率）をそのまま返す。

### 対応ゲート

単一量子ビット: `X`, `H`, `Z`, `Y`。制御ゲート: `CH`, `CX`, `CZ`。トフォリゲート: `CCX`。

### セットアップ

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

### デプロイ

`build.sh` / `render.yaml` により Render へのデプロイを想定。

### ライセンス

MIT License ([LICENSE](./LICENSE)) — Copyright (c) 2026 Kota Mizuno
