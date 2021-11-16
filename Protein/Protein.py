#
# The first version of our function!
# Write doc strings 
#

class Protein:


    def __init__(self, ID = None, name = None, metrics = None, AAsequence = None, file = None):
        self.ID = ID
        self.name = name
        self.metrics = metrics
        self._AAsequence = AAsequence
        self.fasta_file = file
        self._identifier = None
        self._df = None
    
    
    def open_fasta_file(self, file = None):
        if file != None:
            self.fasta_file = file
        aa_seq = []                 
        with open(self.fasta_file) as f:
            for line in f:                          
                aa_seq.append(line)   
        sequence = []
        for i, line in enumerate(aa_seq):         
            line = line.replace("\n","")                
            if line.startswith(">"):               
                identifier = line.replace(">","")
            else:
                for aa in line:
                    sequence += aa                 
        self._AAsequence = sequence
        self._identifier = identifier
        return [self._identifier, self._AAsequence]

    @property
    def AAsequence(self):
        if self.fasta_file == None:
            print("no .fasta file")
        else:
            self._AAsequence = self.open_fasta_file(self.fasta_file)[1]
            return self._AAsequence
    @property
    def identifier(self):
        if self.fasta_file == None:
            print("no .fasta file")
        else:
            self._identifier = self.open_fasta_file(self.fasta_file)[0]
            return self._identifier
    

    def create_df(self):
        list = []
        if self.fasta_file == None and self.metrics == None:
            print("missing metrics or .fasta file")
        else:
            self._AAsequence = self.open_fasta_file(self.fasta_file)[1]
            for x in self._AAsequence:
                metric = {}
                for key, value in self.metrics.items():
                    metric.update({key: value[x]})
                list.append(metric)
            self._df = pd.DataFrame(list)
            return self._df


        
    def averaging_metric(self, metric, window_size):
        self._df = self.create_df()
        window = deque([], maxlen=window_size)
        average = []
        for pos, aa in enumerate(self.AAsequence):
            value = self._df[metric][pos]
            window.append(value)
            average.append(sum(window)/len(window))
        return average

    def plot(self, metric = "hydropathy", window_size = 5):
        self._df = self.create_df()
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
                x = self._df.index,
                y = np.array(average),
                hovertext="Name:"+self._df["Name"] + "<br />" +\
                        "abbr.:" + self._df["3-letter code"]+ ", " + self._df["1-letter code"]
            )
        ]

        fig = go.Figure(data = data, layout = layout)
        return fig.show()


        
