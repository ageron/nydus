# Copyright 2011 DISQUS
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from binascii import crc32

from nydus.db.routers import BaseRouter

class PartitionRouter(BaseRouter):
    def get_db(self, pool, func, key=None, *args, **kwargs):
        # Assume first argument is a key
        if not key:
           return range(len(pool))
        return [crc32(str(key)) % len(pool)]
