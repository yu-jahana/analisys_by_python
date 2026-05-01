
# 1. データの読み込み
df = pd.read_csv('ohtani_2025.csv')

# 2. バットに当たってインプレーになったデータに絞る
df_in_play = df[df['description'] == 'hit_into_play'].copy()

# 3. 「ゴロアウト」と「長打」を分類するラベルを作成
def classify_hit(row):
    # 長打（ホームラン、三塁打、二塁打）
    xbh_events = ['home_run', 'triple', 'double']
    # アウト（凡退、併殺、フォースアウト）
    out_events = ['field_out', 'grounded_into_dp', 'force_out']
    
    if pd.isna(row['events']) or pd.isna(row['bb_type']):
        return 'その他'
        
    if row['events'] in xbh_events:
        return '長打'
    elif row['events'] in out_events and row['bb_type'] == 'ground_ball':
        return 'ゴロアウト'
    else:
        return 'その他'

df_in_play['hit_category'] = df_in_play.apply(classify_hit, axis=1)

# 分析対象の2つのカテゴリーだけに絞る
df_analysis = df_in_play[df_in_play['hit_category'].isin(['長打', 'ゴロアウト'])]

# グラフの日本語文字化け対策（環境に合わせて使ってね）
# plt.rcParams['font.family'] = 'Meiryo' # Windows
# plt.rcParams['font.family'] = 'Hiragino Maru Gothic Pro' # Mac

# 4. 可視化の実行
fig = plt.figure(figsize=(14, 6))

# --- ① コースの比較（ストライクゾーンの散布図） ---
ax1 = fig.add_subplot(1, 2, 1)

# 長打とゴロアウトで色とマーカーを分ける
sns.scatterplot(
    data=df_analysis,
    x='plate_x',
    y='plate_z',
    hue='hit_category',
    style='hit_category',
    palette={'長打': 'red', 'ゴロアウト': 'blue'},
    markers={'長打': 'X', 'ゴロアウト': 'o'},
    s=100,
    alpha=0.8,
    ax=ax1
)

# ストライクゾーンとホームベースの描画
rect = patches.Rectangle((-0.83, 1.5), 1.66, 2.0, linewidth=2, edgecolor='black', facecolor='none', linestyle='--')
ax1.add_patch(rect)
home_plate = patches.Polygon([(-0.708, 0.25), (0.708, 0.25), (0.708, 0), (0, -0.5), (-0.708, 0)],
                             closed=True, edgecolor='black', facecolor='lightgray')
ax1.add_patch(home_plate)

ax1.set_xlim(-3, 3)
ax1.set_ylim(-0.5, 5)
ax1.set_aspect('equal')
ax1.set_title('コース比較：ゴロアウト vs 長打')
ax1.set_xlabel('Horizontal Location (ft)')
ax1.set_ylabel('Vertical Location (ft)')
ax1.legend(loc='upper right')

# --- ② ゴロアウトを取れた「球種」のカウント ---
ax2 = fig.add_subplot(1, 2, 2)

# ゴロアウトのデータだけを抽出
df_goro = df_analysis[df_analysis['hit_category'] == 'ゴロアウト']

# 球種ごとのゴロアウト数をカウントして棒グラフに
sns.countplot(
    data=df_goro,
    x='pitch_name',
    order=df_goro['pitch_name'].value_counts().index, # 多い順に並び替え
    palette='Blues_r',
    ax=ax2
)

ax2.set_title('ゴロアウトを打たせた球種ランキング')
ax2.set_xlabel('Pitch Type')
ax2.set_ylabel('ゴロアウトの数')
ax2.tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.show()