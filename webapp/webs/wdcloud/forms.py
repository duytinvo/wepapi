from typing import List
from typing import Optional

from fastapi import Request


class DocCreateForm:
    def __init__(self, request: Request):
        self.request: Request = request
        self.errors: List = []
        self.caption: Optional[str] = None
        self.text: Optional[str] = None

    async def load_data(self):
        form = await self.request.form()
        self.caption = form.get("caption")
        self.text = form.get("text")

    def is_valid(self):
        if not self.text or not len(self.text) >= 20:
            self.errors.append("Text too short")
        if not self.errors:
            return True
        return False
