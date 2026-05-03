# ohtani-analysis-2025

## 背景
毎年打ちまくる大谷翔平の弱点はないのか単純に知りたくなった

## やったこと
大谷翔平選手の打撃データから弱点はあるのか、自分が敵チーム監督なら抑えるためにどういう指示を出すか考えてみた

## 使用したデータ
MLB公式（Statcast）に溜まっている2025年の大谷翔平の打撃データ

https://baseballsavant.mlb.com/

## 言語
Python

## 事前準備
### 1. Statcast にある全打者データを抽出
```
! pip install pybaseball
from pybaseball import statcast_batter
```

### 2. 全打者の打撃データから大谷の ID（660271）を使用し大谷のデータだけ抽出
```
# 大谷選手の打者データ抽出
shohei_ohtani = 660271
data = statcast_batter('2025-03-30', '2025-10-01', shohei_ohtani)
```

### 3. CSV 化
```
data.to_csv('judge_2025.csv')
```

### 4. 必要なライブラリをインポートして準備完了
```
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.patches as patches

! pip install japanize-matplotlib
import japanize_matplotlib
```