"""CLI entry point: python -m peshitta_roots"""

import webbrowser
import threading
from .app import app

if __name__ == '__main__':
    print("Starting Peshitta Root Finder...")
    print("Building root index from corpus (this may take a moment)...")
    threading.Timer(2.0, lambda: webbrowser.open('http://localhost:8080')).start()
    app.run(debug=False, host='0.0.0.0', port=8080)
