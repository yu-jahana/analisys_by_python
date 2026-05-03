## 対右 / 左ピッチャー毎のボール球空振り率

# 1. データの読み込み
df = pd.read_csv('ohtani_2025.csv')

# 2. ボール球（ゾーン外）の定義
# Statcastの一般的な定義：xは-0.83~0.83以外、zは1.5~3.5以外
is_outside_zone = (df['plate_x'] < -0.83) | (df['plate_x'] > 0.83) | \
                  (df['plate_z'] < 1.5) | (df['plate_z'] > 3.5)

# ゾーン外の投球データだけを抽出
df_chase = df[is_outside_zone].copy()

# 3. スイング判定
swing_descriptions = ['swinging_strike', 'foul', 'hit_into_play', 'swinging_strike_blocked', 'foul_tip']
df_chase['is_swing'] = df_chase['description'].isin(swing_descriptions)

# 4. 可視化
fig, axes = plt.subplots(1, 2, figsize=(16, 8), sharey=True)
sides = [('R', '対 右ピッチャー'), ('L', '対 左ピッチャー')]

for i, (side, title) in enumerate(sides):
    ax = axes[i]
    data_subset = df_chase[df_chase['p_throws'] == side]
    
    # ボール球に対する「スイング率」を計算
    chase_rate = data_subset['is_swing'].mean() * 100
    
    # 散布図（スイング＝赤、見逃し＝青）
    sns.scatterplot(
        data=data_subset,
        x='plate_x',
        y='plate_z',
        hue='is_swing',
        palette={True: 'red', False: 'blue'},
        alpha=0.6,
        ax=ax,
        legend=True if i == 1 else False
    )
    
    # ストライクゾーンの枠
    rect = patches.Rectangle((-0.83, 1.5), 1.66, 2.0, linewidth=2, edgecolor='black', facecolor='none')
    ax.add_patch(rect)
    
    ax.set_xlim(-3, 3)
    ax.set_ylim(0, 5)
    ax.set_title(f'{title}\nボール球スイング率: {chase_rate:.1f}%')
    ax.set_xlabel('Horizontal Location (ft)')
    if i == 0:
        ax.set_ylabel('Vertical Location (ft)')

plt.tight_layout()
plt.show()
