import asyncio
from bson import ObjectId
from pprint import pprint

import uvicorn
from pydantic import BaseModel

from app.ai_agents import main
from app.db import db
from app.repo import BuildRepo
from app.schemas.component_schema import Build


if __name__ == "__main__":
    asyncio.run(main())

# if __name__ == "__main__":
#     build_id = ObjectId("683b7ab21fbad55848727e64")
#     cpu_id = ObjectId("68266380ffe1e50a2f711435")

#     repo = BuildRepo(db)

#     build = repo.load(build_id)
#     print(build)

#     repo.add_component(build_id, "cpu", cpu_id)

#     build = repo.load(build_id)
#     print(build)


# if __name__ == "__main__":
#     """"""

#     build_id = ObjectId("683b7ab21fbad55848727e64")
#     cpu_id = ObjectId("68266380ffe1e50a2f711435")

#     repo = BuildRepo(db)

#     build = repo.get_full_build(build_id)

#     print(build)

#     # print("\n\n")
#     # pprint(list(build)[0])

#     build_model = Build(**build)
#     pprint(build_model.model_dump(exclude_none=True))
