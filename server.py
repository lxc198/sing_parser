# -*- coding: utf-8 -*-
# @Time: 2025/11/10 10:52
# @Author: lxc
# @File: server.py
# @Software: PyCharm

import sanic
from SingParser import SingParser
from setting import get_config_value

app = sanic.Sanic("SingParser")
sp = SingParser()


@app.route("/parse")
async def parse(request):
    url = request.args.get("url")
    if not url:
        return sanic.response.json({"error": "url is required"}, status=400)
    try:
        result = await sp.parse(url)
    except Exception as e:
        return sanic.response.json({"msg": 400, "error": str(e)}, status=400)
    return sanic.response.json({"msg": 200, "data": result})


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=get_config_value("server", "port"), workers=1)
