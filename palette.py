
from pathlib import Path
import argparse
import colors
import csv

# パーサを作る
parser = argparse.ArgumentParser()
parser.add_argument(
    '-o',
    '--out',
    help='出力用CSVファイルパス',
    default='output.csv',
    required=True
)
#引数を解析
args = parser.parse_args()

# 処理を行いたいディレクトリのパス
directory_path = Path( str( Path.cwd() ) + '\palettes' )

#最終的に出力するCSVファイルのパス
output_path = Path( args.out )
# ディレクトリ内の.pngファイルをすべて検索
png_files = directory_path.glob( '*.png' )

#出力用CSVファイルを確認
if not output_path.exists():
    with open( f'{output_path}', 'w', newline='' ) as outcsvfile:
        writer = csv.writer( outcsvfile )
        # ヘッダーを書き込む
        writer.writerow( ['R', 'G', 'B', 'H', 'L', 'S', 'Count'] )

# 各ファイルに対して処理を行う
for file_path in png_files:

    # ここにファイルに対する処理を書く
    colors.pickup( file_path )
    colors.diff( output_path, file_path )
    colors.new( output_path, file_path )
    colors.merge( output_path, file_path )
