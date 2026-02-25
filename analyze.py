import re
from collections import Counter
import jieba
import matplotlib.pyplot as plt
import matplotlib
from datetime import datetime

# 支持中文显示
matplotlib.rcParams['font.family'] = 'Arial Unicode MS'

# ── 读取文件 ──────────────────────────────────────────
with open("data/[LINE]ciel.txt", "r", encoding="utf-8") as f:
    lines = f.readlines()

# ── 解析每一行 ─────────────────────────────────────────
messages = []
current_date = None

for line in lines:
    line = line.strip()
    if not line:
        continue
    
    date_match = re.match(r"(\d{4}\.\d{2}\.\d{2})", line)
    if date_match:
        current_date = date_match.group(1)
        continue
    
    msg_match = re.match(r"(\d{2}:\d{2})\s+(\S+)\s+(.*)", line)
    if msg_match and current_date:
        messages.append({
            "date": current_date,
            "hour": int(msg_match.group(1).split(":")[0]),
            "sender": msg_match.group(2),
            "content": msg_match.group(3)
        })

print(f"总共解析到 {len(messages)} 条消息\n")

# ── 1. 谁发的更多 ──────────────────────────────────────
sender_count = Counter(m["sender"] for m in messages)
print("📊 消息数量：")
for sender, count in sender_count.most_common():
    print(f"  {sender}: {count} 条")

# ── 2. 每天消息数量 ────────────────────────────────────
date_count = Counter(m["date"] for m in messages)
dates = sorted(date_count.keys())
counts = [date_count[d] for d in dates]

plt.figure(figsize=(12, 4))
plt.plot(dates, counts, color='hotpink', linewidth=2)
plt.title("每天消息数量")
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig("analysis/每天消息数量.png", dpi=150)
plt.close()
print("\n✅ 图表已保存：每天消息数量.png")

# ── 3. 最活跃时间段 ────────────────────────────────────
hour_count = Counter(m["hour"] for m in messages)
hours = list(range(24))
hour_counts = [hour_count.get(h, 0) for h in hours]

plt.figure(figsize=(10, 4))
plt.bar(hours, hour_counts, color='hotpink')
plt.title("最活跃时间段")
plt.xlabel("小时")
plt.ylabel("消息数")
plt.xticks(hours)
plt.tight_layout()
plt.savefig("analysis/最活跃时间段.png", dpi=150)
plt.close()
print("✅ 图表已保存：最活跃时间段.png")

# ── 4. 最常用的词 ──────────────────────────────────────
all_text = " ".join(m["content"] for m in messages)
# 过滤掉图片/贴图等系统消息
all_text = re.sub(r"\[.*?\]", "", all_text)

words = jieba.cut(all_text)
# 过滤掉单字和标点
stop = set("的了我你他她是在和就不都有这也很啊哦哈嗯呢吧啦吗噢诶")
word_count = Counter(w for w in words if len(w) > 1 and w not in stop)

print("\n💬 最常用的20个词：")
for word, count in word_count.most_common(20):
    print(f"  {word}: {count}次")

plt.figure(figsize=(10, 5))
top_words = word_count.most_common(20)
plt.barh([w[0] for w in top_words], [w[1] for w in top_words], color='hotpink')
plt.title("最常用的词 Top 20")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("analysis/最常用词.png", dpi=150)
plt.close()
print("✅ 图表已保存：最常用词.png")