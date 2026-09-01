def calculate_route(*, origin, destination, algorithm='MANUAL'):
    """Interface for a future routing provider; no route data is fabricated here."""
    raise NotImplementedError('Route calculation will be integrated in a future phase.')


def optimize_route(route):
    """Interface for a future optimization service."""
    raise NotImplementedError('Route optimization will be integrated in a future phase.')