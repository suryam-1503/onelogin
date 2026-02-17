class FinancialsWaiter: 
    def __init__(self, page): 
        self.page = page 
async def wait(self): 
    await self.page.wait_for_selector("text=Bills", timeout=30000)