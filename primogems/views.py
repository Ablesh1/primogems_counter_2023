from django.shortcuts import render
from django.http import HttpResponse
import datetime
import calendar
from .forms import MyForm


def primogems(request):
    if request.method == "GET":
        form = MyForm()

    return HttpResponse(render(request, "primogems/primogems_new.html", {"form": form}))


def initialize(request):
    if request.method == "POST":
        form = MyForm(request.POST)
        if form.is_valid():
            # Extract the input data from the form
            date_input = form.cleaned_data["date_input"]
            welkin_input = form.cleaned_data["welkin_input"]
            primogems_input = form.cleaned_data["primogems_input"]
            starglitter_input = form.cleaned_data["starglitter_input"]
            pity_input = form.cleaned_data["pity_input"]
            events_input = form.cleaned_data["events_input"]
            quests_input = form.cleaned_data["quests_input"]
            abyss_input = form.cleaned_data["abyss_input"]
            others_input = form.cleaned_data["others_input"]
            # Call the main() method with the input data
            result = main(
                date_input,
                welkin_input,
                primogems_input,
                starglitter_input,
                pity_input,
                events_input,
                quests_input,
                abyss_input,
                others_input,
            )
        else:
            result = None
    else:
        result = None

    return render(
        request, "primogems/primogems_new.html", {"form": form, "result": result}
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


def count_star_glitter(primo, star_glitter, pity):
    pulls_number = primo // 160

    # Pity affects the number of golden star glitter
    if pulls_number + pity >= 90:
        golden = (pulls_number + pity) // 90
    else:
        golden = pulls_number // 90

    silver = (pulls_number - golden * 10) // 10
    star_glitter = golden * 10 + silver * 2 + star_glitter

    return star_glitter


# Here the primogems are calculated
def count(
    amount,
    star,
    is_welkin,
    pity,
    years_left,
    months_left,
    days_left,
    abyss_left,
    events,
    quests,
    abyss_mean,
    others,
):
    # Basic methods of acquiring primogems
    daily_tasks = days_left * 60
    abyss = abyss_left * abyss_mean
    paimon_bargains = months_left * 5 * 160

    # Check if welkin is purchased
    if is_welkin:
        welkin = days_left * 90
    else:
        welkin = 0

    # Accumulated primo (up to date) including actual + actual based star glitter
    total = amount + others
    actual_star = count_star_glitter(total, star, pity)
    accumulated = total + actual_star // 5 * 160

    # Final future amount of star glitter
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
    final_star = count_star_glitter(total, star, pity)

    # Future amount of primo
    total = total + final_star // 5 * 160

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

    # Starglitter used to buy pulls
    glitter_used = final_star - final_star % 5
    glitter_unused = final_star % 5

    print("\nGlitter used: \t\t" + str(glitter_used))
    print("Glitter unused: \t" + str(glitter_unused))

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

    result = [
        accumulated,
        earned,
        total,
        accumulated // 160,
        earned // 160,
        total // 160,
        days_left,
        months_left,
        years_left,
        glitter_used,
        glitter_unused,
    ]
    return result


# Here the variables are passed to multiple functions,
# the returns of which are passed to count()
def start(a, s, w, p, y, m, d, e, q, abm, o):
    years_left = count_years(y)
    months_left = count_months(y, m)
    days_left = count_days(y, m, d)
    abyss_left = count_abyss(days_left, months_left)

    return count(
        a, s, w, p, years_left, months_left, days_left, abyss_left, e, q, abm, o
    )


# Here we assign values to the variables that are passed to start()
def main(
    input_date,
    input_welkin,
    input_primogems,
    input_starglitter,
    input_pity,
    input_events,
    input_quests,
    input_abyss_mean,
    input_others,
):
    # Split the input_data string into components
    components = str(input_date).split("-")

    # Assign components to variables (assuming the input format is always '%Y-%m-%d')
    input_year = int(components[0])
    input_month = int(components[1])
    input_day = int(components[2])

    return start(
        input_primogems,
        input_starglitter,
        input_welkin,
        input_pity,
        input_year,
        input_month,
        input_day,
        input_events,
        input_quests,
        input_abyss_mean,
        input_others,
    )
