! pip install pybaseball
from pybaseball import statcast_batter
# 大谷選手の打者データ抽出
aaron_judge = 592450
shohei_ohtani = 660271
data = statcast_batter('2025-03-30', '2025-10-01', shohei_ohtani)
data.to_csv('ohtani_2025.csv')

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib.patches as patches

! pip install japanize-matplotlib
import japanize_matplotlib