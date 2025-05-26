from jinja2 import Template

from prompt.system import (
    CONSULTANT_SYSTEM_PROMPT,
    EXTRACT_FILTERS_SYSTEM_PROMPT,
    SCHEMAS,
    FILTER_EXAMPLES,
)


template = Template(EXTRACT_FILTERS_SYSTEM_PROMPT)

res = template.render(
    schemas=SCHEMAS,
    examples=FILTER_EXAMPLES,
)

print(res)
