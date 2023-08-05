# timetravel

A simple utility for bulk shifting all event dates in your calendar.

Shift to a specific date in reference to the first or last event in the calendar
or by a certain number of days either forward or backward .

    from timetravel import machine
    machine('cal.ics', shift='20161108', event='first')

`machine` will output a new calendar next to the source file appended with
today's date.

For a summary, just enable `report`.

    machine('cal.ics', report=True)

    ('Events Modified', ':', 3)
    ('Days Traveled', ':', 7)
    ('Origination', ':', '20161101')
    ('Destination', ':', '20161108')

See the example [jupyter notebook][1] or parse [docstring][2] for more info.

[1]: https://github.com/bmweiner/timetravel/blob/master/example/example.ipynb
[2]: https://github.com/bmweiner/timetravel/blob/master/timetravel/parse.py#L10
