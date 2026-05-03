## どういう投球の組み立てが苦手 / 得意なのか出してみた
## 空振りした球種、球速とその一球前は何か


# 1. データの読み込み
df = pd.read_csv('ohtani_2025.csv')

# 2. 1球前のデータ（球種・コース・結果）を紐付け
# 打席(at_bat_number)が変わらない範囲で、1球前の情報をシフトして取得
df = df.sort_values(['game_date', 'at_bat_number', 'pitch_number'])
df['prev_pitch_name'] = df.groupby('at_bat_number')['pitch_name'].shift(1)
df['prev_plate_x'] = df.groupby('at_bat_number')['plate_x'].shift(1)
df['prev_plate_z'] = df.groupby('at_bat_number')['plate_z'].shift(1)

# 3. トンネリングの定義：1球前と今の球のコースが近い（距離1フィート以内）ケースを抽出
df['dist_from_prev'] = ((df['plate_x'] - df['prev_plate_x'])**2 + 
                        (df['plate_z'] - df['prev_plate_z'])**2)**0.5

# トンネル効果が期待できるデータ（コースが近い投球）に絞る
tunnel_df = df[df['dist_from_prev'] < 1.0].copy()

# 4. 空振り判定
whiff_descriptions = ['swinging_strike', 'swinging_strike_blocked', 'foul_tip']
tunnel_df['is_whiff'] = tunnel_df['description'].isin(whiff_descriptions)

# 5. 球種のコンボ（前回の球 → 今回の球）ごとの空振り率を集計
combo_stats = tunnel_df.groupby(['prev_pitch_name', 'pitch_name']).agg(
    count=('is_whiff', 'count'),
    whiffs=('is_whiff', 'sum')
).reset_index()

combo_stats['whiff_rate'] = (combo_stats['whiffs'] / combo_stats['count']) * 100

# 試行回数が少ないコンボを除外して、空振り率が高い順に並べる
combo_top = combo_stats[combo_stats['count'] > 5].sort_values('whiff_rate', ascending=False).head(10)

# 6. 可視化
plt.figure(figsize=(12, 7))
# コンボ名を「前 → 次」という形式にする
combo_top['combo_label'] = combo_top['prev_pitch_name'] + ' \n→ ' + combo_top['pitch_name']

sns.barplot(data=combo_top, x='combo_label', y='whiff_rate', palette='viridis')
plt.title('大谷攻略：残像（トンネリング）を活かした最強の球種コンボ')
plt.xlabel('投球コンボ（1球前 → 今の球）')
plt.ylabel('スイング時の空振り率 (%)')
plt.ylim(0, 100)
plt.grid(axis='y', linestyle='--', alpha=0.7)
plt.tight_layout()
plt.show()
