"""Route for project."""
import views


def init_routes(app):
    """
    Initialize view and it route.

    Args:
        app: instance of application
    """
    app.router.add_route('POST', '/signup', views.register)
