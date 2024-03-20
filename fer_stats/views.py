import numpy as np
from django.shortcuts import render
import plotly.express as px
import pandas as pd

from .models import Record
from .forms import DateForm

from django.contrib.auth.decorators import login_required

from datetime import datetime


@login_required()
def fer_stats_view(request):

    form = DateForm()

    start_date = request.GET.get('start')
    end_date = request.GET.get('end')

    emotions = [(1, "Злость"), (2, "Отвращение"), (3, "Страх"), (4, "Радость"), (6, "Грусть"), (7, "Удивление")]

    charts = []
    counts = []

    for eid, emotion in emotions:
        #print(eid)
        #print(emotion)

        records = Record.objects.filter(emotion_id=eid, user_id=request.user.pk)
        if start_date:
            records = records.filter(date_time__gte=start_date)
        if end_date:
            records = records.filter(date_time__lte=end_date)


        records_df = pd.DataFrame({'date': [r.date_time for r in records], 'emotion_count': np.ones(len(records))})
        records_count = len(records)
        if not records_df['date'].empty:
            records_df['date'] = records_df['date'].dt.strftime('%m/%d/%Y')
            records_df = records_df.groupby('date').count()
            records_df = records_df.reset_index()
            #print(records_df)

        fig = px.bar(
            records_df,
            x='date',
            y='emotion_count',
            title=emotion,
            labels={'date': 'Дата', 'emotion_count': 'Частота'}
        )
        if records_count == 0:
            charts.append("")
        else:
            charts.append(fig.to_html())

        counts.append(records_count)

    context = {
        "form": form,

        "chart_angry": charts[0],
        "chart_disgust": charts[1],
        "chart_fear": charts[2],
        "chart_happy": charts[3],
        "chart_sad": charts[4],
        "chart_surprise": charts[5],

        "count_angry": counts[0],
        "count_disgust": counts[1],
        "count_fear": counts[2],
        "count_happy": counts[3],
        "count_sad": counts[4],
        "count_surprise": counts[5],
    }

    return render(request, "fer_stats/fer_stats.html", context)
