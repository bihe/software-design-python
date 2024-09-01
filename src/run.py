import os

import restaurant_app

if __name__ == "__main__":
    app = restaurant_app.create_app()
    app.run(host=os.getenv("FLASK_RUN_HOST", "localhost"), port=os.getenv("FLASK_RUN_PORT", "9000"))
