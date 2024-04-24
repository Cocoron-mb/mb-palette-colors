# mb-palette-colors
Mabinogi染色パレットにある色をカウントしてCSVファイルを作成します。

## ファイルのダウンロード
[こちらからCSVファイルをダウンロードできます](https://github.com/Cocoron-mb/mb-palette-colors/releases/latest)

## 簡単な説明
CSVファイルは、1つの色につき1行で
R(赤), G(緑), B(青), H(色相), L(輝度), S(彩度), Count(数) 
の列を持っています。

Count(数)はこれまでカウントした最大数になっています。
毎回生成されるパレット毎に異なり、出現しない場合(数=0)もあります。

> [!IMPORTANT]
> 新しい色があったりや数が違うこともあり得ると思っています。

## Googleスプレッドシートで使う
GoogleスプレッドシートにCSVファイルを読み込ませて
- A列の背景色をRGBに合わせて変更
- I列に色相のグループ
- J列に輝度のグループ
- K列にRGBの範囲(最大値-最小値)

を追加して使っています。

[こんなかんじ](https://docs.google.com/spreadsheets/d/11dDPD0g-bclea3AUwqR5GCOq9M6HpD7ObkjAdniGl10/edit?usp=sharing)

### A列の背景色をRGBに合わせて変更

```
function colorCells() {
  var sheet = SpreadsheetApp.getActiveSpreadsheet();
  var values = sheet.getRange('A:D').getValues();

  for (var i = 1; i < values.length; i++) {
    var row = values[i];
    var cell = sheet.getRange('A' + (i + 1));
    cell.setBackgroundRGB(row[1], row[2], row[3]);
  }
}
```

こんなスクリプトでA列の背景色をB～D列のRGB値になるように変更しています。

### I列に色相のグループ

```
=ROUNDUP(mod(E2+15,360)/30)
```

E列にある色相の値を30度づつグループにして、近しい色で絞り込みやすくしています。

### J列に輝度のグループ

```
=ROUNDUP((F2-17)/34)
```

G列にある輝度の値を4等分し、明るさが近い色で絞り込みやすくしています。

### K列にRGBの範囲(最大値-最小値)

```
=max(B2, C2, D2)-min(B2, C2, D2)
```

RGB各値の範囲(最大値と最小値の差)です。

グレーを探したいときに使います。理想的なグレー(範囲=0)は数が少ないので,
許容できる範囲まで広げて絞り込んでいます。5～10位で使っています。

### 表全体の行の並び替え
RGB値で並び変えると綺麗にならないので、J列、I列を優先に(以下G, F, E, B, C, D列)で並び替えています。

## カウントする人へ

1.パレット画像を用意し、palettesフォルダに置いておく
> [!NOTE]
> カーソルや検索結果などが写っていないパレット部分のみのPNG画像 (254x254pxサイズ)

2.プログラムを実行する
```
py ./palette.py -o (CSVファイル名)
```

## 連絡先
不具合、他に便利な使い方などありましたら、Twitterだったものでお知らせ頂けると嬉しいです。


[![Twitter URL](https://img.shields.io/twitter/url/https/twitter.com/CocoronRf.svg?style=social&label=%20%40CocoronRf)](https://twitter.com/CocoronRf)
