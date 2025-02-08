import locale
import datetime

locale.setlocale(locale.LC_ALL, 'ru-Ru')

d = datetime.date(2025, 2, 9)

print(d.strftime("%b"))