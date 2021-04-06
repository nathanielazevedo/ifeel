from quickchart import QuickChart
import datetime


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


def analyzeUserFoods(foods):
    greatlist = []
    okaylist = []
    badlist = []
    today = []
    week = []
    month = []
    monthAgo = datetime.datetime.now() - datetime.timedelta(30)
    weekAgo = datetime.datetime.now() - datetime.timedelta(7)
    dayAgo = datetime.datetime.now() - datetime.timedelta(1)
    for each in foods:

        if (each.timestamp > monthAgo):
            month.append(each)

        if (each.timestamp > weekAgo):
            week.append(each)

        if (each.timestamp > dayAgo):
            today.append(each)

    for each in month:
        if each.feeling == '3':
            greatlist.append(int(each.feeling))
        if each.feeling == '2':
            okaylist.append(int(each.feeling))
        if each.feeling == '1':
            badlist.append(int(each.feeling))

    total = len(month)
    greats = len(greatlist)
    okays = len(okaylist)
    bads = len(badlist)
    timeFrame = "Past Month"
    graph = makeGraph(total, greats, okays, bads, timeFrame)

    greatlist.clear()
    okaylist.clear()
    badlist.clear()

    for each in week:
        if each.feeling == '3':
            greatlist.append(int(each.feeling))
        if each.feeling == '2':
            okaylist.append(int(each.feeling))
        if each.feeling == '1':
            badlist.append(int(each.feeling))
    total = len(week)
    greats = len(greatlist)
    okays = len(okaylist)
    bads = len(badlist)
    timeFrame = "Past Week"
    graph3 = makeGraph(total, greats, okays, bads, timeFrame)

    greatlist.clear()
    okaylist.clear()
    badlist.clear()

    for each in today:
        if each.feeling == '3':
            greatlist.append(int(each.feeling))
        if each.feeling == '2':
            okaylist.append(int(each.feeling))
        if each.feeling == '1':
            badlist.append(int(each.feeling))
    total = len(today)
    greats = len(greatlist)
    okays = len(okaylist)
    bads = len(badlist)
    timeFrame = "Past Day"
    graph2 = makeGraph(total, greats, okays, bads, timeFrame)
    return graph, graph2, graph3
