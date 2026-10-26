from litestar import Litestar
from litestar.config.cors import CORSConfig
from litestar.openapi import OpenAPIConfig
from app.api.routes import routes
from app.models import migrate
app=Litestar(route_handlers=routes,on_startup=[migrate],cors_config=CORSConfig(allow_origins=['http://localhost:5173','http://localhost:8080'],allow_methods=['GET','POST'],allow_headers=['Authorization','Content-Type']),openapi_config=OpenAPIConfig(title='Synthetic MSME Underwriting Desk',version='0.1.0'),request_max_body_size=11*1024*1024,debug=False)
