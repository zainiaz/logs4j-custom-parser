import plotly.express as px
"""
    Users plotpy and a panda dataframe to generate graphs and other
    chats (under development to add more options)
"""

class Plotter:
    def __init__(self):
        self.initiated = True
    
    def is_initiated(self):
        if self.initiated:
            return True
        else:
            return False
    
    def plot(self, panda_dataframe, name): 
        try:
            fig = px.line(panda_dataframe)
            
            fig.update_layout({"title": 'Logs',
                        "xaxis": {"title":"Dates"},
                        "yaxis": {"title":"Frequencies"},
                        "showlegend": True})
            fig.write_html(f"{name}.html")
            
            return True
        except:
            return False