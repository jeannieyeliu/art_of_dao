# Art of Dao

This project contains three main scripts for divination and tarot reading: `throw_money.py`, `tarot_gui.py`, and `tarot_cli.py`.

## Project Overview

- `throw_money.py`: A script for I Ching divination using the coin tossing method.
- `tarot_gui.py`: A graphical user interface for tarot card readings.
- `tarot_cli.py`: A command-line interface for tarot card readings.

## Requirements

- Python 3.9 or higher
- pip (Python package installer)

## Environment Setup

1. Clone the repository:
   ```
   git clone https://github.com/jeannieyeliu/art_of_dao.git
   cd art_of_dao
   ```

2. (Optional) Create and activate a virtual environment:
   ```
   python3 -m venv dao_env
   source dao_env/bin/activate  # On Windows, use `dao_env\Scripts\activate`
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Running the Scripts

### throw_money.py

To run the I Ching divination script:

```
python3 throw_money.py
```

### tarot_gui.py

To run the tarot card reading GUI:

```
python3 tarot_gui.py
```

### tarot_cli.py

To run the tarot card reading CLI:

```
python3 tarot_cli.py
```

## PyCharm Configuration

To configure these scripts in PyCharm:

1. Open the project in PyCharm.
2. Go to Run > Edit Configurations.
3. Click the '+' button and select 'Python'.
4. Set up a configuration for each script:
   - Name: Choose a name (e.g., "Throw Money", "Tarot GUI", "Tarot CLI")
   - Script path: Select the respective .py file
   - Python interpreter: Choose your project interpreter
5. Click 'Apply' and 'OK'.

Now you can run each script from the PyCharm interface using the configurations you've set up.

## Note

Make sure you have the necessary image files for the tarot cards in the `TarotCards` directory for the tarot scripts to work properly.

If you encounter any issues or have questions, please open an issue on the GitHub repository.
