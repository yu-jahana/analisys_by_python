# 1. データの読み込み
df = pd.read_csv('ohtani_2025_v2.csv')

# 2. 「アウト」と「ヒット」を分類
# hit_value（H）かアウト（Out）かを判別するフラグを作成
def classify_result(row):
    hit_events = ['single', 'double', 'triple', 'home_run']
    out_events = ['field_out', 'force_out', 'grounded_into_dp', 'fielders_choice', 'field_error']
    
    if row['events'] in hit_events:
        return 'ヒット'
    elif row['events'] in out_events:
        return 'アウト'
    else:
        return None

df['result_category'] = df.apply(classify_result, axis=1)

# 分析対象（ヒット or アウト）だけに絞り込み
df_plot = df[df['result_category'].notna()].copy()

# 3. 可視化の実行
fig = plt.figure(figsize=(16, 8))

# --- ① コースの比較（ヒット vs アウト） ---
ax1 = fig.add_subplot(1, 2, 1)

sns.scatterplot(
    data=df_plot,
    x='plate_x',
    y='plate_z',
    hue='result_category',
    style='result_category',
    palette={'ヒット': 'red', 'アウト': 'blue'},
    markers={'ヒット': 'X', 'アウト': 'o'},
    s=80,
    alpha=0.6,
    ax=ax1
)

# ストライクゾーンの枠
rect = patches.Rectangle((-0.83, 1.5), 1.66, 2.0, linewidth=2, edgecolor='black', facecolor='none', linestyle='--')
ax1.add_patch(rect)
# ホームベース
home_plate = patches.Polygon([(-0.708, 0.25), (0.708, 0.25), (0.708, 0), (0, -0.5), (-0.708, 0)],
                             closed=True, edgecolor='black', facecolor='lightgray')
ax1.add_patch(home_plate)

ax1.set_xlim(-2.5, 2.5)
ax1.set_ylim(-0.5, 5)
ax1.set_aspect('equal')
ax1.set_title('コース別：ヒット vs アウト の分布')
ax1.set_xlabel('Horizontal Location (ft)')
ax1.set_ylabel('Vertical Location (ft)')

# --- ② 球種別の内訳（積み上げ棒グラフ） ---
ax2 = fig.add_subplot(1, 2, 2)

# 球種ごとのカウントを計算
pitch_counts = df_plot.groupby(['pitch_name', 'result_category']).size().unstack(fill_value=0)
# 合計ヒット数が多い順に並び替え
pitch_counts['total'] = pitch_counts.sum(axis=1)
pitch_counts = pitch_counts.sort_values('total', ascending=False).drop(columns='total')

pitch_counts.plot(kind='bar', stacked=True, color=['#3498db', '#e74c3c'], ax=ax2)

ax2.set_title('球種別：アウトとヒットの割合')
ax2.set_xlabel('Pitch Type')
ax2.set_ylabel('Count')
ax2.tick_params(axis='x', rotation=45)
ax2.legend(title='結果')

plt.tight_layout()
plt.show()