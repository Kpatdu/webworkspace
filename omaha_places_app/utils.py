from calendar import HTMLCalendar

class Calendar(HTMLCalendar):
    '''
    Class to generate a calendar for the specified month and year.
    '''

    def __init__(self, year = None, month = None):
        self.year = year
        self.month = month
        super(Calendar, self).__init__(firstweekday = 6) # Set the first day of the week to Sunday


    def formatday(self, day, events):
        '''
        Return a day as a table cell.
        '''

        events_per_day = events.filter(start_time__day = day)
        cal_day = ''

        for event in events_per_day:
            cal_day += f'<li> {event.get_html_url} </li>'

        if day != 0:
            return f'<td><span class="date">{day}</span><ul> {cal_day} </ul></td>'

        return '<td></td>'


    def formatweek(self, the_week, events):
        '''
        Return a complete week as a table row.
        '''

        cal_week = ''

        for cal_day, _ in the_week:
            cal_week += self.formatday(cal_day, events)

        return f'<tr> {cal_week} </tr>'


    def formatmonth(self, events, withyear = True):
        '''
        Return a formatted month as a table.
        '''

        event_calendar = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
        event_calendar += f'{self.formatmonthname(self.year, self.month, withyear = withyear)}\n'
        event_calendar += f'{self.formatweekheader()}\n'

        for week in self.monthdays2calendar(self.year, self.month):
            event_calendar += f'{self.formatweek(week, events)}\n'

        return event_calendar
