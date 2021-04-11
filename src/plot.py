import numpy as np
import matplotlib.pyplot as plt

# Algorithm one- no one is sure.
# Algorithm     Diff: mu = 3.20, CI = 0.31
# Algorithm      Rel: mu = 4.04, CI = 0.21
#
# Algorithm two - all is sure.
# Algorithm     Diff: mu = 2.99, CI = 0.37
# Algorithm      Rel: mu = 4.29, CI = 0.22
#
#
# Algorithm 3 - least confident generated
# Diff: mu = 3.14, CI = 0.33
# Rel: mu = 4.03, CI = 0.24
#
# Algorithm 4 - most confident generated
# Diff: mu = 3.29, CI = 0.28
# Rel: mu = 3.46, CI = 0.36


labels = ['A', 'B', 'C', 'D']
diff_means = [3.2, 2.99, 3.14, 3.29]
diffs_ci = (0.31, 0.37, 0.33, 0.28)
rel_means = [4.04, 4.29, 4.03, 3.46]
rel_ci = (0.21, 0.22, 0.24, 0.36)

x = np.arange(len(labels)) + [0, 0, 1, 1]  # the label locations
width = 0.35  # the width of the bars

fig, ax = plt.subplots()
rects1 = ax.bar(x - width / 2, diff_means, width, label='Difficulty', yerr=diffs_ci)
rects2 = ax.bar(x + width / 2, rel_means, width, label='Relevance', yerr=rel_ci)

# Add some text for labels, title and custom x-axis tick labels, etc.
ax.set_ylabel('Scores')
# ax.set_title('Scores by group and gender')
ax.set_xticks(x)
ax.set_xticklabels(labels)
ax.legend()

ax.bar_label(rects1, padding=3)
ax.bar_label(rects2, padding=3)

# fig.tight_layout()

# plt.figtext(0.05, 0.01, 'A - Ensemble Uncertainty    B - Ensemble least Confidence', fontsize=10)
# plt.figtext(0.1, 0.0, 'A - Ensemble Low Probability Ratio \nB - High\n', fontsize=10, )
plt.annotate('A - Ensemble Low Probability Ratio \nB - High', (0,0), (0, -18), xycoords='axes fraction', textcoords='offset points', va='top')
plt.annotate('C - Low Probability Ratio.Generated \nD - High', (0,0), (220, -18), xycoords='axes fraction', textcoords='offset points', va='top')
plt.show()
