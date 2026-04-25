# 1. データの読み込み
df = pd.read_csv('ohtani_2025_v2.csv')

# 2. インプレーの打球データのみ抽出（座標があるもの）
df_spray = df[df['hc_x'].notna() & df['hc_y'].notna()].copy()

# 3. ヒットとアウトを分類
def classify_hit_or_out(row):
    hit_events = ['single', 'double', 'triple', 'home_run']
    if row['events'] in hit_events:
        return 'ヒット'
    else:
        return 'アウト'

df_spray['result'] = df_spray.apply(classify_hit_or_out, axis=1)

# 4. 可視化（スプレーチャート）
plt.figure(figsize=(10, 10))

# 散布図の描画（hc_yは上下逆転させる必要がある場合が多いので調整）
sns.scatterplot(
    data=df_spray,
    x='hc_x',
    y='hc_y',
    hue='result',
    style='result',
    palette={'ヒット': 'red', 'アウト': 'blue'},
    markers={'ヒット': 'X', 'アウト': 'o'},
    s=100,
    alpha=0.7
)

# グラウンドの簡易的な線を引く（野球場っぽく見せるため）
# ※Statcastの座標系は 0-250 程度。本塁は (125, 200) 付近。
plt.plot([125, 25], [200, 100], color='black', lw=1)  # 三塁線
plt.plot([125, 225], [200, 100], color='black', lw=1) # 一塁線
plt.plot([25, 125, 225], [100, 10, 100], color='black', lw=1, linestyle='--') # 外野フェンス風

# グラフの設定
plt.gca().invert_yaxis() # y軸を反転させて本塁を下に
plt.title('大谷選手：打球方向分布（スプレーチャート）')
plt.xlabel('Horizontal Location')
plt.ylabel('Vertical Location')
plt.legend(title='結果')
plt.axis('equal')
plt.grid(False)

plt.show()