from bokeh.plotting import figure, output_file, save

# prepare some data
import json
data = json.load(open("cg_speed.json"))

# create a new plot with a title and axis labels
p = figure(title="Training Time", x_axis_label='Factors', y_axis_label='Seconds')

# prepare some data
to_plot = [(data['cg2'], "CG (2 Steps/Iteration)", "#2ca02c"),
           (data['cg3'], "CG (3 Steps/Iteration)", "#ff7f0e"),
#           (data['cg4'], "CG (4 Steps/Iteration)", "#d62728"),
           (data['cholesky'], "Cholesky", "#1f77b4")]

# use bokek to plot out the result, saving the graph
p = figure(title="Training Speed", x_axis_label='Factors', y_axis_label='Time / Iteration (s)')
for current, label, colour in to_plot:
    p.line(data['factors'], current, legend=label, line_color=colour, line_width=1)
    p.circle(data['factors'], current, legend=label, line_color=colour, size=6, fill_color="white")

p.legend.location = "top_left"

save(p, "cg_training_speed.html", title="CG ALS Training Speed")
