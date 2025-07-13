# import asyncio
# from bson import ObjectId
# from pprint import pprint

# import uvicorn
# from pydantic import BaseModel

# from app.ai_loop import main
# from app.db import db
# from app.repos.component_repo import BuildRepo, ChatRepo
# from app.schemas.component_schema import Build
# from app.schemas.pyobjectid import PyObjectId


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


# if __name__ == "__main__":
#     chat_repo = ChatRepo(db)
#     res = chat_repo.update_history(PyObjectId("683b7ab21fbad55848727e64"), "hello")
#     print(res)
