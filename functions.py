from quickchart import QuickChart


symptoms = ['acid reflux', 'diarrhea', 'constipation', 'heart burn', 'bloating', 'naseau', 'gas', 'upset stomach', 'abdominal pain', 'cramps', 'vomitting']





qc = QuickChart()
qc.width = 500
qc.height = 300
qc.device_pixel_ratio = 2.0

def makeGraph(total, greats, okays, bads):
    qc.config = {
        "type": 'doughnut',
        "data": {
            "datasets": [
            {
                "data": [bads, okays, greats],
                "backgroundColor": [
                'rgb(255, 99, 132)',
                'rgb(255, 205, 86)',
                'rgb(75, 192, 192)',
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
                                {"text":'total inputs'}],
    }}}}
    return qc.get_short_url()

def makeEmptyGraph():
    qc.config = {
        "type": 'doughnut',
        "data": {
            "datasets": [
            {
                "data": [1,1,1],
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
                                {"text":'Eat Some Food'}],
    }}}}

    return qc.get_short_url()

    
{
        "type": "bar",
        "data": {
            "labels": ["Hello world", "Test"],
            "datasets": [{
                "label": "Foo",
                "data": [1, 2]
            }]
        }
    }