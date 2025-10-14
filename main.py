import requests
import login
from to_ics import build_ics
cookies = login.get_cookies();
params = {
    'start_date': '2025-01-01T16:00:00.000Z',
    'order': 'aesc',
    'per_page': '1000000',
}

response = requests.get('https://elearning.fudan.edu.cn/api/v1/planner/items', params=params, cookies=cookies)
data = response.json();
items = [];
for i in data:
    if(i["plannable_type"]=="assignment" and not i.get("submissions", {}).get("submitted", True)):
        name = i["plannable"]["title"]
        ddl = i["plannable"]["due_at"]
        course = i["context_name"]
        items.append({name:[ddl,course]})
print(items);
# Example data from your message

ics_content = build_ics(items, "Asia/Taipei")

# Write to file for download
output_path = "assignments.ics"
with open(output_path, "w", encoding="utf-8") as f:
    f.write(ics_content)
