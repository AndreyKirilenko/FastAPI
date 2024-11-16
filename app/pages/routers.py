from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates


pages_router = APIRouter(prefix='/pages', tags=['Фронтенд'])
templates = Jinja2Templates(directory='templates')


@pages_router.get('/admin')
async def get_admin_html(request: Request):
    # import ipdb; ipdb.set_trace()
    return templates.TemplateResponse(name='admin.html', context={'request': request})
