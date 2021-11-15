#
# The first version of our function!
# Write doc strings 
#

class Protein:

    def __init__(self, ID = "not known", 
                name = "not known", 
                metrics = "not known", 
                fasta_file = "not known", 
                AAsequence = "not known",
                identifier = "not known"):
        self.ID = ID
        self.name = name
        self.metrics = metrics
        self.fasta_file = fasta_file
        self.AAsequence = AAsequence
        self.identifier = identifier
    
    def open_fasta_file(self, file = None):
        if self.fasta_file == "not known":
            self.fasta_file = file
        self.AAsequence = open_fasta_file(self.fasta_file)[1]
        self.identifier = open_fasta_file(self.fasta_file)[0]

    def create_df(self):
        list = []
        for x in self.AAsequence:
            metric = {}
            for key, value in self.metrics.items():
                metric.update({key: value[x]})
            list.append(metric)
        self.df = pd.DataFrame(list)

    def averaging_metric(self, metric, window_size):

        window = deque([], maxlen=window_size)
        average = []
        for pos, aa in enumerate(self.AAsequence):
            value = self.df[metric][pos]
            window.append(value)
            average.append(sum(window)/len(window))
        return average

    def plot(self, metric = "hydropathy", window_size = 1):

        if metric == "hydropathy":
            metric = "hydropathy index (Kyte-Doolittle method)"

        layout = {"title": {"text": "{0}, averaging window size: {1}".format(self.name, window_size)},
                "template" : "plotly", 
                "yaxis": {"title": {"text": metric}},
                "xaxis": {"title": {"text": "amino acid position"}}
                }

        average = self.averaging_metric(metric, window_size = window_size)

        data = [
            go.Bar(
                x = self.df.index,
                y = np.array(average),
                hovertext="Name:"+self.df["Name"] + "<br />" +\
                        "abbr.:" + self.df["3-letter code"]+ ", " + self.df["1-letter code"]
            )
        ]

        fig = go.Figure(data = data, layout = layout)
        return fig.show()

        
