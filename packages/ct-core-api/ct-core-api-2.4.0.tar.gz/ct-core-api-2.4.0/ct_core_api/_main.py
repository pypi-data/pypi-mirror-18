#!/usr/bin/env python
from ct_core_api.api.app import runner
from ct_core_api.api.app.factory import create_api_app

app = create_api_app(__name__)


if __name__ == '__main__':
    runner.run(app)
