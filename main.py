import uvicorn, vk, pymongo

from fastapi import Depends, FastAPI, Request, Response
from pydantic import BaseSettings

class Settings(BaseSettings):
    confirmation_string: str
    vk_token: str
    group_id: int
    admin_id: int
    sqlite_config: str
    class Config:
        env_file = ".env"

settings = Settings()

vk_session = vk.Session(access_token=settings.vk_token)
vk_api = vk.API(vk_session)

client = MongoClient('localhost', 27017)
db = client['WorkoutBot']

async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session

app = FastAPI()

@app.post("/main")
async def authorize(req: Request, session: AsyncSession = Depends(get_session)):
    req_body = await req.json()
    print(req_body)
    if req_body['type'] == 'adminpanel':
        if req_body['type2'] == 'send_msgs':
            await admin_panel.send_msgs(vk_api, req_body['group'], req_body['msg'], session)
    elif req_body['type'] == 'confirmation' and req_body['group_id'] == settings.group_id:
        return Response(content=settings.confirmation_string, media_type="application/json")
    elif req_body['type'] == 'message_new':
        if "payload" in req_body["object"]["message"]:
            pd = req_body["object"]["message"]["payload"]
            if pd == '{"command":"start"}':
                await grand.start(vk_api, req_body["object"]["message"]["from_id"])
            if eval(pd).get("command") in ["friends", "classmates", "programmers"]:
                await grand.add_to_group(vk_api, req_body["object"]["message"]["from_id"], eval(pd).get("command"), session)
        else:
            if '/' in req_body['object']['message']['text']:
                await grand.add_phrase_command(
                    req_body['object']['message']['text'],
                    vk_api, 
                    req_body['object']['message']['from_id'],
                    session)
            else:
                await grand.reply_to_message(
                    req_body['object']['message']['text'],
                    vk_api, 
                    req_body['object']['message']['from_id'],
                    session)
        return Response('ok', media_type="application/json")

if __name__ == '__main__':
    uvicorn.run("main:app", port=5000, reload=True)