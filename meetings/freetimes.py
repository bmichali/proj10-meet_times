
import flask
import logging
import arrow
from flask_main import interpret_time, interpret_date

def list_events(service, calendar):
    """
    Based on the calendar, return a list of events, events are all the events inside that calendar.
    Each event is represented by a dict.
    """
    logging.debug("Entering list_events")
    logging.debug(interpret_time(flask.session['begin_time'])
                     + " " + interpret_time(flask.session['end_time']))

    found_events = []
    found_freetimes = []
    days = arrow.Arrow.range('day', arrow.get(flask.session['begin_date']),
                             arrow.get(flask.session['end_date']))

    startHour, startMin = flask.session['begin_time'].split(":")
    endHour, endMin = flask.session['end_time'].split(":")

    for day in days:
        timeMin = day.replace(hour=int(startHour), minute=int(startMin))
        timeMax = day.replace(hour=int(endHour), minute=int(endMin))
        eventList = service.events().list(calendarId=calendar,singleEvents=True,
                                          timeMin=timeMin, timeMax=timeMax).execute()["items"]
        temp_day = []
        for event in eventList:
            if "transparency" in event:
                continue
            else:
                if "dateTime" in event["start"]:
                    start = event["start"]["dateTime"]
                    end = event["end"]["dateTime"]
                else:
                    start = event["start"]["date"]
                    end = event["start"]["date"]

                if "description" in event:
                    summary = event["description"]
                else:
                    summary = "(N/A)"

                temp_event = {
                        "start": arrow.get(start).isoformat(),
                        "end": arrow.get(end).isoformat(),
                        "summary": summary
                    }

                temp_day.append(temp_event)
                found_events.append(temp_event)

        # if there are no events for current day, grab timeMin to timeMax
        if len(temp_day) == 0:
            hours, minutes, start, end = getDiff(timeMin, timeMax)
            addFreetime(found_freetimes, start, end, hours, minutes)
        else:
            counter = 0
            for event in temp_day:
                # if first event of the day, grab timeMin and start time of current
                if counter == 0:
                    hours, minutes, start, end = getDiff(
                        timeMin, arrow.get(event["start"]))
                    addFreetime(found_freetimes, start, end, hours, minutes)
                    counter = counter + 1
                # if last event of the day, grab end time of current, and timeMax
                if counter == len(temp_day):
                    hours, minutes, start, end = getDiff(
                        arrow.get(event["end"]), timeMax)
                    addFreetime(found_freetimes, start, end, hours, minutes)
                # if it isn't last or first, grab end time of current and start time of next
                else:
                    hours, minutes, start, end = getDiff(
                        arrow.get(event["end"]), arrow.get(temp_day[counter]["start"]))
                    addFreetime(found_freetimes, start, end, hours, minutes)
                    counter = counter + 1

        # logging.debug(found_events)
        # logging.debug(found_freetimes)
    return found_events, found_freetimes

def getDiff(start, end):
    # if the timedelta isn't negative, find duration
    if start < end:
        diff = end - start
        logging.debug(str(start) + " " + str(end))
        logging.debug("length: " + str((diff.seconds) // 60))
        hours = diff.seconds // 3600
        minutes = (diff.seconds % 3600) // 60
        return hours, minutes, start, end
    else:
        return 0, 0, start, end

def addFreetime(list, start, end, hours, minutes):
    # if time slot is larger than 15 mins(default), add to list
    if minutes >= 15 or hours > 0:
        list.append(
            {
                "start": start.isoformat(),
                "end": end.isoformat(),
                "duration": str(hours) + " hours " + str(minutes) + " mins"
            })
        logging.debug("Found Freetime: " + str(hours) + " hours " + str(minutes) + " mins")