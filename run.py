"""
Application Entry Point
=======================
Runs the Flask application
"""

import os
from app import create_app

# Get configuration from environment variable or default to development
config_name = os.getenv('FLASK_ENV', 'development')

# Create application instance
app = create_app(config_name)

if __name__ == '__main__':
    # Get host and port from config
    host = app.config.get('HOST', '0.0.0.0')
    port = app.config.get('PORT', 5000)
    debug = app.config.get('DEBUG', True)

    print(f"""
    ╔═══════════════════════════════════════════════════════════╗
    ║   Inventory Management System                              ║
    ║   Running on: http://{host}:{port}                   ║
    ║   Environment: {config_name}                               ║
    ║   Debug Mode: {debug}                                      ║
    ╚═══════════════════════════════════════════════════════════╝
    """)

    # Run the application
    app.run(
        host=host,
        port=port,
        debug=debug
    )
