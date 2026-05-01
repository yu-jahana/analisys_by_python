# 1. データの読み込み
df = pd.read_csv('ohtani_2025.csv')

# 2. カウント（ボール-ストライク）を文字列で作成
df['count'] = df['balls'].astype(str) + '-' + df['strikes'].astype(str)

# 3. 指標の計算
# スイングしたかどうかの判定 (descriptionに 'strike' が含まれ、かつ見逃しでないもの、または 'hit_into_play')
swing_descriptions = ['swinging_strike', 'foul', 'hit_into_play', 'swinging_strike_blocked', 'foul_tip']
df['is_swing'] = df['description'].isin(swing_descriptions)

# 空振りしたかどうかの判定
whiff_descriptions = ['swinging_strike', 'swinging_strike_blocked', 'foul_tip']
df['is_whiff'] = df['description'].isin(whiff_descriptions)

# カウントごとの集計
count_stats = df.groupby('count').agg(
    total_pitches=('pitch_name', 'count'),
    swings=('is_swing', 'sum'),
    whiffs=('is_whiff', 'sum')
).reset_index()

# 指標の算出
count_stats['swing_pct'] = (count_stats['swings'] / count_stats['total_pitches']) * 100
count_stats['whiff_pct'] = (count_stats['whiffs'] / count_stats['swings']) * 100 # スイングに対する空振り率

# データ数がある程度多いカウントに絞る（ノイズ除去）
count_stats = count_stats[count_stats['total_pitches'] > 10]

# 表示順を野球のカウントっぽく整理
count_order = ['0-0', '1-0', '2-0', '3-0', '0-1', '1-1', '2-1', '3-1', '0-2', '1-2', '2-2', '3-2']
count_stats['count'] = pd.Categorical(count_stats['count'], categories=count_order, ordered=True)
count_stats = count_stats.sort_values('count')

# 4. 可視化
fig, ax1 = plt.subplots(figsize=(12, 6))

# Swing % の棒グラフ
sns.barplot(data=count_stats, x='count', y='swing_pct', color='skyblue', alpha=0.7, ax=ax1, label='Swing % (積極性)')
ax1.set_ylabel('Swing % (スイング率)')
ax1.set_ylim(0, 100)

# Whiff % の折れ線グラフ（2軸目）
ax2 = ax1.twinx()
sns.lineplot(data=count_stats, x='count', y='whiff_pct', color='red', marker='o', linewidth=2, ax=ax2, label='Whiff % (空振り率)')
ax2.set_ylabel('Whiff % (スイング時の空振り率)')
ax2.set_ylim(0, 100)

plt.title('大谷選手：カウント別の積極性と空振り率')
ax1.grid(axis='y', linestyle='--', alpha=0.5)
fig.legend(loc='upper right', bbox_to_anchor=(1, 1), bbox_transform=ax1.transAxes)

plt.tight_layout()
plt.show()