import asyncio


class BaseApplication:
    def __init__(self, *, config, **kwargs):
        self.config = kwargs.pop('config', None)

    def run_forever(self, **kwargs):
        loop = self.loop

        print("======== Running aioworkers ========\n"
              "(Press CTRL+C to quit)")

        try:
            loop.run_forever()
        except KeyboardInterrupt:
            pass
        loop.close()


class Application(BaseApplication, dict):
    def __init__(self, *, loop, config, **kwargs):
        if loop is None:
            loop = asyncio.get_event_loop()
        self.loop = loop
        super().__init__(config=config)
