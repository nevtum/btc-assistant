from mangum import Mangum

from manage import create_app

app = create_app()

lambda_handler = Mangum(app)
