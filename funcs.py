from dateutil import parser
import re
import debug

# Rough check for strings that *look like* dates
# Accept both full and abbreviated month names
DATE_KEYWORDS = [
    "January", "February", "March", "April", "May", "June",
    "July", "August", "September", "October", "November", "December",
    "Jan", "Feb", "Mar", "Apr", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
]

def looks_like_date(s):
    return any(month in s for month in DATE_KEYWORDS) and re.search(r"\d{4}", s)

def monthStrToWeekdayNum(date_str):
    if not looks_like_date(date_str):
        # debug.log.error(f"IGNORED NON-DATE STRING `{date_str}`")
        return -1
    try:
        date_obj = parser.parse(date_str)
        return date_obj.weekday()  # 0 = Monday
    except Exception:
        # debug.log.warning(f"COULD NOT PARSE DATE `{date_str}` - should be recognizable format: returning -1 to void this article")
        return -1
