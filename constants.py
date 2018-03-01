import itertools

# COSTANTS
jira_export_filename = "data/backlog.csv"
jira_base_url = "https://jira.skatelescope.org/browse/"
board_name = "PI planning"
epics_list_name = "epics"
backlog_list_name = "backlog"
label_colors = ['yellow', 'purple', 'blue', 'green', 'orange',
                'black', 'sky', 'pink', 'lime']
story_points = ['0', '0.5', '1', '2', '3', '5', '8', '13', '20', '40', '100']
story_points_color = 'red'
# cycling iterator over available colors
color = itertools.cycle(label_colors)
