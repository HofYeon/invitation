from django import template
from datetime import date
from django.utils import timezone
register = template.Library()
_KOR_WD = ["월","화","수","목","금","토","일"]

@register.filter
def ko_full_datetime(dt):
    if not dt:
        return ""
    dt = timezone.localtime(dt)

    h = dt.hour
    # 12시간 값
    hour12 = (h % 12) or 12

    # AM/PM 라벨 (원래 로직 유지: 12시는 '낮')
    ampm = "낮" if h == 12 else ("오전" if h < 12 else "오후")

    return f"{dt.year}년 {dt.month}월 {dt.day}일 {_KOR_WD[dt.weekday()]}요일 {ampm} {hour12}시 {dt.minute:02d}분"

@register.filter
def d_day(value):
    """value: datetime or date"""
    if not value:
        return ""
    target = value.date() if hasattr(value, "date") else value
    today = date.today()
    delta = (target - today).days
    return f"D-{delta}" if delta > 0 else ("D-Day" if delta == 0 else f"D+{abs(delta)}")