## 対右 / 左ピッチャー毎の空振り率

# 1. データの読み込み
df = pd.read_csv('ohtani_2025.csv')

# 2. 空振り(swinging_strike)のデータに絞る
# 苦手 ＝ 「バットが空を切った」という定義で分析するよ！
df_whiff = df[df['description'] == 'swinging_strike'].copy()

# 3. 可視化の実行
# 右投げ(R)と左投げ(L)で左右に並べて比較するよ
fig, axes = plt.subplots(1, 2, figsize=(16, 8), sharey=True)

throws = [('R', '右ピッチャー'), ('L', '左ピッチャー')]

for i, (side, title) in enumerate(throws):
    ax = axes[i]
    data_subset = df_whiff[df_whiff['p_throws'] == side]
    
    # ヒートマップ風に空振りの密度を可視化（どこで空振りを取っているか）
    sns.kdeplot(
        data=data_subset,
        x='plate_x',
        y='plate_z',
        fill=True,
        thresh=0.05,
        levels=10,
        cmap='Reds',
        alpha=0.6,
        ax=ax
    )
    
    # 個別の空振り地点を散布図で重ねる（球種ごとに色分け）
    sns.scatterplot(
        data=data_subset,
        x='plate_x',
        y='plate_z',
        hue='pitch_name',
        s=40,
        alpha=0.7,
        palette='tab10',
        ax=ax
    )

    # ストライクゾーンの枠を描画
    rect = patches.Rectangle((-0.83, 1.5), 1.66, 2.0, linewidth=2, edgecolor='black', facecolor='none')
    ax.add_patch(rect)
    
    # ホームベース
    home_plate = patches.Polygon([(-0.708, 0.25), (0.708, 0.25), (0.708, 0), (0, -0.5), (-0.708, 0)],
                                 closed=True, edgecolor='black', facecolor='lightgray')
    ax.add_patch(home_plate)

    ax.set_xlim(-2.5, 2.5)
    ax.set_ylim(-0.5, 5)
    ax.set_title(f'{title} vs 大谷：空振り発生エリア')
    ax.set_xlabel('Horizontal Location (ft)')
    if i == 0:
        ax.set_ylabel('Vertical Location (ft)')
    
    # 凡例の設定
    ax.legend(title='球種', bbox_to_anchor=(1.05, 1), loc='upper left', fontsize='small')

plt.tight_layout()
plt.show()
