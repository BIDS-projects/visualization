from visualization import app
import os

if __name__ == '__main__':
    app.run(int(os.environ.get('PORT', 5000)), debug=True)
