from django.shortcuts import render
from django.http import HttpResponse
import datetime
import calendar
from .forms import MyForm


def primogems(request):
    if request.method == "GET":
        form = MyForm()

    return HttpResponse(
        render(request, "primogems/primogems_page.html", {"form": form})
    )


def initialize(request):
    if request.method == "POST":
        form = MyForm(request.POST)
        if form.is_valid():
            # Extract the input data from the form
            date_input = form.cleaned_data["date_input"]
            primogems_input = form.cleaned_data["primogems_input"]
            starglitter_input = form.cleaned_data["starglitter_input"]
            events_input = form.cleaned_data["events_input"]
            quests_input = form.cleaned_data["quests_input"]
            others_input = form.cleaned_data["others_input"]
            # Call the main() method with the input data
            result = main(
                date_input,
                primogems_input,
                starglitter_input,
                events_input,
                quests_input,
                others_input,
            )
        else:
            result = None
    else:
        result = None

    return render(
        request, "primogems/primogems_page.html", {"form": form, "result": result}
    )


# Primogems Counter class
class Primogems:
    def __init__(
        self,
        actual_amount,
        daily_tasks,
        welkin,
        spiral_abyss,
        paimon_bargains,
        star_glitter,
        events,
        quests,
        others,
    ):
        self.actual_amount = actual_amount
        self.daily_tasks = daily_tasks
        self.welkin = welkin
        self.spiral_abyss = spiral_abyss
        self.bargains = paimon_bargains
        self.star_glitter = star_glitter
        self.events = events
        self.quests = quests
        self.others = others

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)


def count_days(y1, m1, d1):
    today = datetime.date.today()
    someday = datetime.date(y1, m1, d1)
    diff = someday - today
    days_left = diff.days

    return days_left


def count_months(y2, m2):
    act_month = datetime.datetime.now().month
    act_year = datetime.datetime.now().year

    if act_year == y2:
        months_left = m2 - act_month
    else:
        months_left = 12 - act_month + m2 + 12 * (y2 - act_year - 1)

    return months_left


def count_years(y3):
    act_year = datetime.datetime.now().year
    years_left = y3 - act_year

    return years_left


def count_abyss(period, months_left):
    now = datetime.datetime.now()
    abyss_left = 0
    add = -1

    days_of_month = calendar.monthrange(now.year, now.month)[1]
    days_of_months_left = days_of_month - now.day

    """
    print("\nDays of month: " + str(days_of_month))
    print("Days of month left: " + str(days_of_months_left))
    print("\nPeriod: " + str(period))
    print("Abyss: " + str(abyss_left))
    """

    # New abyss starts in the 1st and the 16th day of each month
    # We consider that ongoing abyss is done for current month
    # Current month:
    if days_of_months_left >= 16 and (now.day + period) >= 16:
        abyss_left += 1
        period -= days_of_months_left

    elif days_of_months_left < 16 and (now.day + period) >= 16:
        period -= days_of_months_left

    else:
        period = 0

    # All months after current one, starting from 1st day
    for _ in range(0, months_left):
        diff_months = calendar.monthrange(now.year, 1 + (now.month + 1 + add) % 12)[1]

        if period >= diff_months:
            abyss_left += 2
            period -= diff_months
        elif 16 <= period < diff_months:
            abyss_left += 2
            period -= period
        elif 1 <= period < 16:
            abyss_left += 1
            period -= period

        add += 1

        """
        print("\nDays of month: " + str(diff_months))
        print("Months analyzed: " + str(add))
        print("Period: " + str(period))
        print("Abyss: " + str(abyss_left))
        """

    return abyss_left


def count_list(my_list):
    list_left = 0
    for i in range(0, len(my_list)):
        list_left += my_list[i]
    return list_left


def count_star_glitter(primogems, star_glitter):
    pulls_number = primogems // 160
    golden = pulls_number // 90
    silver = (pulls_number - golden * 10) // 10

    star_glitter = golden * 10 + silver * 2 + star_glitter

    return star_glitter


# Here the primogems are calculated
def count(
    amount,
    pulls_done,
    days_left,
    months_left,
    years_left,
    abyss_left,
    star,
    events,
    quests,
    others,
):
    daily_tasks = days_left * 60
    welkin = days_left * 90
    abyss = abyss_left * 450
    paimon_bargains = months_left * 5 * 160

    # Accumulated primo (up to date) including actual + actual based star glitter
    total = amount + others
    star = count_star_glitter(total, star)
    accumulated = total + star // 5 * 160

    # Future amount of star glitter
    total = (
        amount
        + daily_tasks
        + welkin
        + abyss
        + paimon_bargains
        + events
        + quests
        + others
    )
    star = count_star_glitter(total, star)

    # Future amount of primo
    total = total + star // 5 * 160

    # Future amount of earned primo
    earned = total - accumulated

    # Summary
    p = Primogems(
        amount,
        daily_tasks,
        welkin,
        abyss,
        paimon_bargains,
        star // 5 * 160,
        events,
        quests,
        others,
    )

    print("\nDays left:\t\t" + str(days_left))
    print("Months left:\t\t" + str(months_left))
    print("Years left:\t\t" + str(years_left))

    print("\nGlitter used: \t\t" + str(star - star % 5))
    print("Glitter unused: \t" + str(star % 5))

    print("\nPulls done:\t\t" + str(pulls_done))
    print("Pulls left:\t\t" + str(accumulated // 160))

    print("\n" + str(p))
    duplicate = "\tPulls"
    print(
        "Total accumulated:\t"
        + str(accumulated)
        + "\tPrimogems\t-->\t"
        + str(accumulated // 160)
        + duplicate
    )
    print(
        "Total earned:\t\t"
        + str(earned)
        + " \tPrimogems\t-->\t"
        + str(earned // 160)
        + duplicate
    )
    print(
        "Total amount:\t\t"
        + str(total)
        + "\tPrimogems\t-->\t"
        + str(total // 160)
        + duplicate
    )

    result = [accumulated, earned, total, pulls_done, accumulated // 160, total // 160]
    return result


# Here the variables are passed to multiple functions,
# the returns of which are passed to count()
def start(a, p, y, m, d, s, e, q, o):
    days_left = count_days(y, m, d)
    months_left = count_months(y, m)
    years_left = count_years(y)
    abyss_left = count_abyss(days_left, months_left)
    events_left = count_list(e)
    quests_left = count_list(q)
    others_left = count_list(o)

    return count(
        a,
        p,
        days_left,
        months_left,
        years_left,
        abyss_left,
        s,
        events_left,
        quests_left,
        others_left,
    )


# Here we assign values to the variables that are passed to start()
def main(
    input_date,
    input_primogems,
    input_starglitter,
    input_events,
    input_quests,
    input_others,
):
    # Split the input_data string into components
    components = str(input_date).split("-")

    # Assign components to variables (assuming the input format is always '%Y-%m-%d')
    choose_year = int(components[0])
    choose_month = int(components[1])
    choose_day = int(components[2])

    # Assign other input values
    amount_of_primogems = input_primogems
    amount_of_star_glitter = input_starglitter
    amount_of_pulls_done = 0

    events_list = [input_events]
    quests_list = [input_quests]
    others_list = [input_others]

    # Print the variables for debug
    print(f"Date: {input_date}")
    print(f"Year: {choose_year}")
    print(f"Month: {choose_month}")
    print(f"Day: {choose_day}")
    print(f"Primogems: {input_primogems}")
    print(f"StarGlitter: {input_starglitter}")
    print(f"Events: {input_events}")
    print(f"Quests: {input_quests}")
    print(f"Others: {input_others}")

    return start(
        amount_of_primogems,
        amount_of_pulls_done,
        choose_year,
        choose_month,
        choose_day,
        amount_of_star_glitter,
        events_list,
        quests_list,
        others_list,
    )