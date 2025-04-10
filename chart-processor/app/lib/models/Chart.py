class Chart:
    def __init__(self):
        self.chart_name = ''
        self.chart_sequence = ''
        self.pdf_name = ''
        self.pdf_url = ''
        self.did_change = False
        self.change_pdf_name = None
        self.change_pdf_url = None

    def __str__(self):
        return str({
            'chart_name': self.chart_name,
            'chart_sequence': self.chart_sequence,
            'pdf_name': self.pdf_name,
            'pdf_url': self.pdf_url,
            'did_change': self.did_change,
            'change_pdf_name': self.change_pdf_name,
            'change_pdf_url': self.change_pdf_url
        })

    def __repr__(self):
        return self.__str__()
