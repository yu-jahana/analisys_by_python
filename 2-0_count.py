import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.patches as patches

# 1. データの読み込み
df = pd.read_csv('ohtani_2025.csv')

# 2. 2-0カウントかつスイングしたデータに絞り込み
swing_descriptions = ['swinging_strike', 'foul', 'hit_into_play', 'swinging_strike_blocked', 'foul_tip']
df_2_0_swing = df[(df['balls'] == 2) & (df['strikes'] == 0) & (df['description'].isin(swing_descriptions))].copy()

# 3. 結果のフラグ化
df_2_0_swing['swing_result'] = df_2_0_swing['description'].apply(
    lambda x: '空振り' if 'swinging_strike' in x else '空振り以外'
)

# 4. 可視化（ホームベースを追加）
fig, axes = plt.subplots(1, 2, figsize=(16, 9))
results = ['空振り', '空振り以外']

for i, res in enumerate(results):
    ax = axes[i]
    subset = df_2_0_swing[df_2_0_swing['swing_result'] == res]
    
    # 散布図
    sns.scatterplot(data=subset, x='plate_x', y='plate_z', hue='pitch_name', s=120, alpha=0.8, ax=ax, edgecolor='white')
    
    # ストライクゾーン（点線）
    rect = patches.Rectangle((-0.83, 1.5), 1.66, 2.0, linewidth=2, edgecolor='black', facecolor='none', linestyle='--', zorder=2)
    ax.add_patch(rect)
    
    # --- ホームベースの描画（キャッチャー/審判視点） ---
    # plate_x=0 が中心。ホームベースの幅は約17インチ（1.41フィート）。
    # plate_z=0（地面）の位置にベースを書く
    base_x = [-0.708, 0.708, 0.708, 0, -0.708] # 左右の端と尖った先端
    base_z = [0.2, 0.2, 0, -0.2, 0] # 地面付近に厚みを持たせて描画
    # シンプルに五角形を配置
    home_plate = patches.Polygon([
        (-0.708, 0.4), (0.708, 0.4), (0.708, 0.2), (0, 0), (-0.708, 0.2)
    ], closed=True, linewidth=1, edgecolor='gray', facecolor='whitesmoke', zorder=1)
    ax.add_patch(home_plate)
    
    # 軸の設定
    ax.set_xlim(-2.5, 2.5)
    ax.set_ylim(-0.5, 5)
    ax.set_aspect('equal')
    ax.set_title(f'2-0時: {res}の分布 (n={len(subset)})', fontsize=14)
    ax.set_xlabel('Horizontal Location (ft)')
    ax.set_ylabel('Vertical Location (ft)')
    ax.legend(title='球種', bbox_to_anchor=(1.05, 1), loc='upper left')
    ax.grid(True, linestyle=':', alpha=0.6)

plt.tight_layout()
plt.savefig('ohtani_2_0_with_homeplate.png')
plt.show()