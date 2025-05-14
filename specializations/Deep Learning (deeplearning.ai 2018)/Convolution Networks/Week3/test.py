import matplotlib.pylab as plt
from skimage.io import imread
import glob
in_list = glob.glob('in/*')
out_list = glob.glob('out/*')
print in_list, out_list
for i in range(len(in_list)):
	inp = imread(in_list[i])
	plt.figure(figsize=(25,10))
	#plt.autoscale_view('tight')
	plt.subplot(211); plt.axis('off'); plt.imshow(inp); plt.title('Input')
	outp = imread(out_list[i])
	plt.subplot(212); plt.axis('off'); plt.imshow(outp); plt.title('Output')
	#plt.tight_layout()
	plt.subplots_adjust(wspace=0, hspace=0.15)
	plt.savefig('in_out/res_' + in_list[i].split('\\')[1].split('.')[0] + '.png', bbox_inches="tight", pad_inches=0)
	