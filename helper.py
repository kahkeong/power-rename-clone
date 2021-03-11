import datetime
import logging


def replace(path_object, name):
    time = datetime.datetime.fromtimestamp(path_object.stat().st_mtime)
    pattern_value = {
        "$YYYY": time.strftime("%Y"),
        "$YY": time.strftime("%y"),
        "$Y": time.strftime("%y")[-1],
        "$MMMM": time.strftime("%B"),
        "$MMM": time.strftime("%b"),
        "$MM": time.strftime("%m"),
        "$M": time.strftime("%m").lstrip("0"),
        "$DDDD": time.strftime("%A"),
        "$DDD": time.strftime("%a"),
        "$DD": time.strftime("%d"),
        "$D": time.strftime("%d").lstrip("0"),
        "$hh": time.strftime("%H"),
        "$h": time.strftime("%H").lstrip("0"),
        "$mm": time.strftime("%M"),
        "$m": time.strftime("%M").lstrip("0"),
        "$ss": time.strftime("%S"),
        "$s": time.strftime("%S").lstrip("0"),
        "$fff": time.strftime("%f")[:3],
        "$ff": time.strftime("%f")[:2],
        "$f": time.strftime("%f")[:1],
    }

    for key, value in pattern_value.items():
        name = name.replace(key, value)

    logging.debug(f"before: {path_object.name}, after: {name}")
    return name
