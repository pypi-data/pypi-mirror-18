from pyrnkr.artifacts.models import Service

class SampleService(Service):
    required_parameters = []
    name = 'Sample Service'

    def _execute(self, parameters):
        return {}


def handler(event, context):
    return SampleService().run(event)
