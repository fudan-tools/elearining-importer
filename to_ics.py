# Generate an ICS file from a list of {name: [ddl_utc, course]} dicts
from datetime import datetime, timezone
from zoneinfo import ZoneInfo
import uuid

def ics_escape(text: str) -> str:
    """Escape text for ICS (commas, semicolons, backslashes, and newlines)."""
    return (text
            .replace("\\", "\\\\")
            .replace(",", "\\,")
            .replace(";", "\\;")
            .replace("\n", "\\n")
            )

def build_ics(assignments: list, tz_name: str = "Asia/Taipei") -> str:
    tz = ZoneInfo(tz_name)
    now_utc = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

    # VTIMEZONE for Asia/Taipei (no DST)
    vtimezone = (
        "BEGIN:VTIMEZONE\r\n"
        f"TZID:{tz_name}\r\n"
        f"X-LIC-LOCATION:{tz_name}\r\n"
        "BEGIN:STANDARD\r\n"
        "TZOFFSETFROM:+0800\r\n"
        "TZOFFSETTO:+0800\r\n"
        "TZNAME:CST\r\n"
        "DTSTART:19700101T000000\r\n"
        "END:STANDARD\r\n"
        "END:VTIMEZONE\r\n"
    )

    cal = [
        "BEGIN:VCALENDAR",
        "PRODID:-//ChatGPT//Assignment Export//EN",
        "VERSION:2.0",
        "CALSCALE:GREGORIAN",
        vtimezone.strip()
    ]

    for item in assignments:
        for name, (ddl_utc, course) in item.items():
            # Parse ISO 8601 with trailing Z; convert to Asia/Taipei
            dt = datetime.fromisoformat(ddl_utc.replace("Z", "+00:00")).astimezone(tz)
            dt_local_str = dt.strftime("%Y%m%dT%H%M%S")
            uid = f"{uuid.uuid4()}@assignments"
            summary = ics_escape(str(name))
            description = ics_escape(str(course))

            event = [
                "BEGIN:VEVENT",
                f"UID:{uid}",
                f"DTSTAMP:{now_utc}",
                f"DTSTART;TZID={tz_name}:{dt_local_str}",
                f"SUMMARY:{summary}",
                f"DESCRIPTION:{description}",
                "END:VEVENT"
            ]
            cal.extend(event)

    cal.append("END:VCALENDAR")
    return "\r\n".join(cal) + "\r\n"


