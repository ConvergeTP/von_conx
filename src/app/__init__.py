"""
Copyright 2017-2018 Government of Canada - Public Services and Procurement Canada - buyandsell.gc.ca

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from app import cfg
from app.cache import mem_cache
from app.service.bootseq import BootSequence
from app.service.eventloop import do
from sanic import Sanic


# initialize app; load views
app = Sanic(strict_slashes=True)
c = cfg.init_config()
from app import views

@app.listener('before_server_stop')
async def cleanup(app, loop):
    ag = await mem_cache.get('agent')
    if ag is not None:
        await ag.close()

    pool = await mem_cache.get('pool')
    if pool is not None:
        await pool.close()

# start
BootSequence.go()
