import matplotlib.pyplot as plt
import matplotlib.pylab as pylab
import numpy as np
from style import BNM_style as BNM



params = {'font.family': BNM.font.get('font_text_name'),
		'font.size': BNM.font.get('font_text_size'),
		'text.color': BNM.hex_codes.get('Dark grey'), 
         'axes.labelsize': BNM.font.get('data_labels_font_size'),
         'axes.titlesize': BNM.font.get('font_text_size'),
         'axes.edgecolor': BNM.hex_codes.get('Dark grey'),
         'axes.spines.right': False,
         'axes.spines.top': False,
         'axes.labelweight': 'bold',
         'axes.axisbelow': True,
         'xtick.labelsize': BNM.font.get('data_labels_font_size'),
         'ytick.labelsize': BNM.font.get('data_labels_font_size'),
         'lines.color': BNM.hex_codes.get('Light blue'),
         'legend.fontsize': BNM.font.get('data_labels_font_size'),
         'legend.loc': "best",
         'legend.handlelength': 2,
         'savefig.format': 'png'}

pylab.rcParams.update(params)

def summary_bar(y, width, title, xlabel):

	fig, ax = plt.subplots(figsize=(6, 5))

	y_pos = np.arange(len(y))

	ax.set_yticklabels(y)
	ax.set_yticks(y_pos)
	ax.grid(axis='x', zorder=0)

	rects = ax.barh(y = y_pos, width = width, align='center', color = BNM.hex_codes.get('Dark blue'))

	ax.set_title(title,
		loc = 'left',
		fontname = BNM.font.get('font_title_name'),
		y=1.05)

	for i, v in enumerate(width):
		ax.text(v * 1.05, i - 0.25, str(v), color=BNM.hex_codes.get('Magenta'))

	ax.set_xlabel(xlabel)

	plt.subplots_adjust(left=0.35, right=0.9)

	plt.savefig('../Summary_stats.png', dpi=300)
	#plt.show()

def AvP(pred, y_test, r2, alpha):

	plt.plot(range(len(pred)), pred, color = BNM.hex_codes.get('Light blue'), label = 'Predicted')
	plt.plot(range(len(y_test)), y_test, color = BNM.hex_codes.get('Magenta'), label = 'Actual')

	R2 = 'R2 = ' + str(r2)
	alpha = 'alpha = ' + str(alpha)

	#plt.text(25, 6, text)
	plt.title('Actual Vs Pred' + ' , ' + R2 + ' , ' + alpha,loc = 'left',
		fontname = BNM.font.get('font_title_name'),
		y=1.05)
	plt.legend()
	plt.ylabel("Receptiveness score")
	plt.xlabel("Response")
	plt.savefig('../AvP.png', dpi=300)
	#plt.show()


def scatter(df, title, thresh):

	fig, ax = plt.subplots()

	scatter = ax.scatter(df['x'], df['y'],
		c = BNM.hex_codes.get('Dark grey'),
		alpha=0.3,
		label="Sampled data")

	lineplot = ax.plot(df['x'], df['ypred'],
		label="Predicted outcome Y")

	ax.axvline(x=thresh, color = BNM.hex_codes.get('Magenta'))

	ax.set_title(title,
		loc = 'left',
		fontname = BNM.font.get('font_title_name'),
		y=1.05)

	ax.set_xlabel("Forcing variable (x)")
	ax.set_ylabel("Outcome variable (y)")
	ax.legend()

	plt.savefig('../Out/Scatter.png', dpi=300)

	#plt.show()






