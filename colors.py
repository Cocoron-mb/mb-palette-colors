from collections import Counter
from pathlib import Path
import colorsys
import csv
import cv2
import pandas as pd

def select_max_count(row):
    """Countの値が大きい方のH,L,Sの値を選択する関数

    Args:
        行のデータ

    Returns:
        Countの値が大きい方のH,L,Sの値
    """
    # Count_1とCount_2のどちらかが欠損値の場合は、欠損値でない方を返す
    if pd.isna(row['Count_1']):
        return (row['H_2'], row['L_2'], row['S_2'], row['Count_2'])
    elif pd.isna(row['Count_2']):
        return (row['H_1'], row['L_1'], row['S_1'], row['Count_1'])
    # 両方とも欠損値でない場合は、Countの値が大きい方のH,L,Sの値を返す
    else:
        if row['Count_1'] > row['Count_2']:
            return (row['H_1'], row['L_1'], row['S_1'], row['Count_1'])
        else:
            return (row['H_2'], row['L_2'], row['S_2'], row['Count_2'])

def diff( org_file_path: Path, new_file_path: Path ):
    """2つのCSVファイルを比較し
    　Count値が大きい行からできるCSVファイルを出力します

    Args:
        org_file_path ( Path ): 比較元(最終的に出力する)CSVファイルパス
        new_file_path ( Path ): 新しいCSVファイルパス
    """
    # CSVファイルを読み込む
    df1 = pd.read_csv( org_file_path, dtype=int )
    df2 = pd.read_csv( f'{new_file_path.parent}\{new_file_path.stem}.csv', dtype=int )

    # df2にあってdf1にない行、またはdf2の'Count'値がdf1の'Count'値より大きい行を見つける
    df3 = pd.merge(
        df1,
        df2,
        on=['R', 'G', 'B', 'H', 'L', 'S'],
        how='left',
        suffixes=('_df1', '_df2'),
        indicator=True
    )
    df3 = df3.query( 'Count_df1 < Count_df2' )
    # 'merge'列を削除する
    df3 = df3.drop( columns=['_merge'] )
    if len( df3 ) > 0:
        df3.to_csv( f'{new_file_path.parent}\{new_file_path.stem}_change.csv', index=False)

def new( org_file_path: Path, new_file_path: Path ):
    """2つのCSVファイルを比較し
    　新しいCSVファイルのみにある行を出力します

    Args:
        org_file_path ( Path ): 比較元(最終的に出力する)CSVファイルパス
        new_file_path ( Path ): 新しいCSVファイルパス
    """
    # CSVファイルを読み込む
    df1 = pd.read_csv( org_file_path, dtype=int )
    df2 = pd.read_csv( f'{new_file_path.parent}\{new_file_path.stem}.csv', dtype=int )

    # df1とdf2を'Count'列を除いて結合し、重複を削除する
    df_combined = pd.merge(
        df1,
        df2,
        on=['R', 'G', 'B', 'H', 'L', 'S'], 
        how='outer',
        suffixes=('_df1', '_df2'), indicator=True
    )
    # df2にのみ存在する行を取得
    df3 = df_combined[df_combined['_merge'] == 'right_only']

    # 不要な列を削除し、列名を修正する
    df3 = df3.drop(columns=['Count_df1', '_merge'])
    df3 = df3.rename(columns={'Count_df2': 'Count'})

    # 新しいCSVファイルとして出力する
    if len( df3 ) > 0:
        df3.to_csv( f'{new_file_path.parent}\{new_file_path.stem}_new.csv', index=False)

def merge( output_file_path: Path, new_file_path: Path ):
    """2つのCSVファイルを比較し
    　新しいCSVファイルから新しい色、数が多い色を
    　既存のCSVファイルに適用します

    Args:
        output_file_path ( Path ): 最終的に出力するCSVファイルパス
        new_file_path ( Path ): 新しいCSVファイルパス
    """
    # CSVファイルを読み込む
    df1 = pd.read_csv( output_file_path, dtype=int )
    df2 = pd.read_csv( f'{new_file_path.parent}\{new_file_path.stem}.csv', dtype=int )
    # 2つのDataFrameをR,G,Bの列で結合する
    df = pd.merge(df1, df2, on=['R', 'G', 'B'], how='outer', suffixes=('_1', '_2'))
    # Countの値が大きい方のH,L,Sの値を選択する関数を行ごとに適用する
    df['HLS_Count'] = df.apply(select_max_count, axis=1)
    # 出力したい列を選択する
    df = df.loc[:, ['R', 'G', 'B', 'HLS_Count']]
    # 'HLS_Count'の列を展開する
    df[['H', 'L', 'S', 'Count']] = pd.DataFrame(df['HLS_Count'].tolist(), index=df.index, dtype=int)
    # 'HLS_Count'の列を削除する
    df = df.drop( 'HLS_Count', axis=1 )
    # CSVファイルに出力する
    df.to_csv( output_file_path, index=False )

def pickup( file_path ):
    """画像ファイル中の色を取得します

    Args:
        file_path ( str ): 読み込む画像ファイルパス
    """

    # 画像ファイルを読み込む
    img = cv2.imread( str( file_path ) )
    # 画像の色空間をBGRからRGBに変換する
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    # 画像の配列を一次元に変形する
    img = img.reshape(-1, 3)
    # 画像の各色の個数をカウントする
    color_counts = Counter(map(tuple, img))
    # CSVファイルに色と個数を書き込む
    with open(f'{file_path.parent}\{file_path.stem}.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        # ヘッダーを書き込む
        writer.writerow(['R', 'G', 'B', 'H', 'L', 'S', 'Count'])
        # 色と個数をR,G,Bの順で昇順にソートして書き込む
        for color, count in sorted(color_counts.items(), key=lambda x: x[0]):
            # RGB値のタプルを展開してR,G,Bに分ける
            r, g, b = color
            h, l, s = colorsys.rgb_to_hls(r/255, g/255, b/255)
            # R,G,B,Countの順で書き込む
            writer.writerow([r, g, b, int(round(h * 360)), int(round(l * 100)), int(round(s * 100)), count])

