from quickchart import QuickChart


symptoms = ['acid reflux', 'diarrhea', 'constipation', 'heart burn', 'bloating',
            'naseau', 'gas', 'upset stomach', 'abdominal pain', 'cramps', 'vomitting']


qc = QuickChart()
qc.width = 500
qc.height = 300
qc.device_pixel_ratio = 2.0


def makeGraph(total, greats, okays, bads, timeFrame):
    qc.config = {
        "type": 'doughnut',
        "data": {
            "datasets": [
                {
                    "data": [bads, okays, greats],
                    "backgroundColor": [
                        'rgb(255, 99, 132)',
                        'rgb(255, 205, 86)',
                        'rgb(151, 199, 132)',
                    ],
                    "label": 'Dataset 1',
                },
            ],
        },
        "options": {
            "plugins": {
                "doughnutlabel": {
                    "labels": [
                        {
                            "text": total, "font": {
                                "size": 20}},
                        {"text": timeFrame}],
                }}}}
    return qc.get_short_url()


def makeBarGraph(symptoms, symptomslists):
    qc.config = {

        "type": 'horizontalBar',
        "data": {

                "labels": symptoms,
                "datasets": [
                    {
                        "label": 'Number of reports per symptom after eating',
                        "data": symptomslists,
                        "backgroundColor": [
                            'rgb(86, 181, 172)',
                            'rgb(115, 219, 147)',
                            'rgb(225, 130, 86)',
                            'rgb(11, 65, 123)',
                            'rgb(93, 175, 217)',
                            'rgb(182, 220, 160)',
                            'rgb(163, 143, 153)',
                            'rgb(200, 200, 47)',
                            'rgb(29, 139, 151)',
                            'rgb(244, 138, 98)',
                            'rgb(192, 229, 203)',
                        ],
                    }
                ]
        }
    }

    return qc.get_short_url()


def makeEmptyGraph():
    qc.config = {
        "type": 'doughnut',
        "data": {
            "datasets": [
                {
                    "data": [1, 1, 1],
                    "backgroundColor": [
                        'rgb(255, 99, 132)',
                        'rgb(255, 205, 86)',
                        'rgb(75, 192, 192)',
                    ],

                },
            ],
        },
        "options": {
            "plugins": {
                "doughnutlabel": {
                    "labels": [
                        {
                            "text": "You're empty", "font": {
                                "size": 20}},
                        {"text": 'Eat Some Food'}],
                }}}}

    return qc.get_short_url()


def genFoodGraph(fooddata):
    qc.config = {
        "type": 'pie',
        "data": {
            "datasets": [
                {
                    "data": fooddata,
                    "backgroundColor": [
                        'rgb(255, 99, 132)',
                        'rgb(255, 205, 86)',
                        'rgb(75, 192, 192)',
                    ],
                    "label": 'Dataset 1',
                },
            ],
        },
    }
    return qc.get_short_url()
