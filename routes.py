"""Route for project."""
import views


def init_routes(app, cors):
    """
    Initialize view and it route.

    Args:
        app: instance of application
        cors: instance of cors config
    """
    cors.add(
        app.router.add_route('POST', '/signup', views.register),
    )
