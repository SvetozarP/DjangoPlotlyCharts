from django.db.models import Avg
from django.shortcuts import render
from core.models import CO2
import plotly.express as px
from core.forms import DateForm
# Create your views here.


def chart(request):
    co2 = CO2.objects.all()
    start = request.GET.get('start')
    end = request.GET.get('end')

    if start:
        co2 = co2.filter(date__gte=start)
    if end:
        co2 = co2.filter(date__lte=end)

    fig = px.line(
        x=[c.date for c in co2],
        y=[c.average for c in co2],
    )

    fig.update_layout(title={
        'font_size': 22,
        'xanchor': 'center',
        'x': 0.5,
    })

    chart_fig = fig.to_html()

    context = {
        'chart': chart_fig,
        'form': DateForm,
    }

    return render(request, 'core/chart.html', context)


def yearly_avg_co2(request):
    averages = CO2.objects.values('date__year').annotate(avg=Avg('average'))
    xdata = averages.values_list('date__year', flat=True)
    ydata = averages.values_list('avg', flat=True)

    text = [f'{avg:.0f}' for avg in ydata]

    fig = px.bar(x=xdata, y=ydata, text=text)

    fig.update_layout(
        title_text='Average CO2 concentration per Year',
        yaxis_range=[0, 500],
    )

    fig.update_traces(
        textfont_size=16,
        textangle=-90,
        textposition='outside',
        cliponaxis=False,
    )

    chart_fg = fig.to_html()
    context = {'chart': chart_fg}

    return render(request, 'core/chart.html', context)


