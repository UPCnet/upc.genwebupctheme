## Script (Python) "toPloneboardTime"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=time=None
##title=
##
#given a time string convert it into a DateTime and then format it appropariately
from DateTime import DateTime
ploneboard_time=None
ts = context.translation_service
utranslate = context.utranslate

format = '%Y;%m;%d;%w;%H;%M;%S'

# fallback formats, english
young_format_en = '%A %H:%M' 
old_format_en = '%d/%m/%Y %H:%M'


if not time:
    return 'Unknown date'

try:
    if not isinstance(time, DateTime):
        time = DateTime(str(time))
    (year, month, day, wday, hours, minutes, seconds) = time.strftime(format).split(';')
 

    ploneboard_time = utranslate("old_date_format: ${day} ${month} ${year} ${hours}:${minutes}",
                                     {'day':day, 'month':utranslate(ts.month_msgid(month)), 
                                      'year':year, 'hours':hours, 'minutes':minutes},
                                      default=time.strftime(old_format_en))  
 
except IndexError:
    pass 

return ploneboard_time
