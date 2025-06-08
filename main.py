# import uvicorn


# if __name__ == "__main__":
#     uvicorn.run(app="app.app:app", host="localhost", port=8000, reload=True)


import asyncio
from app.ai_agents import main

if __name__ == "__main__":
    asyncio.run(main())
