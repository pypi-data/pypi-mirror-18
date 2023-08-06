from bokeh.plotting import figure, output_file, show, save
import json

data = json.load(open("cg_accuracy.json"))

# prepare some data
x = range(1, 26)
to_plot = [(data['cg2'], "CG (2 Steps/Iteration)", "#2ca02c"), # #d62728
           (data['cg3'], "CG (3 Steps/Iteration)", "#ff7f0e"),
           (data['cholesky'], "Cholesky", "#1f77b4")]

# use bokek to plot out the result, saving the graph
p = figure(title="Training Loss", x_axis_label='Iteration', y_axis_label='MSE')
for data, label, colour in to_plot:
    p.line(x, data, legend=label, line_color=colour, line_width=1)
    p.circle(x, data, legend=label, line_color=colour, size=6, fill_color="white")

save(p, "cg_training_loss.html", title="CG ALS Training Loss")
