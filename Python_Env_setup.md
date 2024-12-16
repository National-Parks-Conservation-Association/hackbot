#### Setting up Python Virtual Environment in VSCode (Windows)

##### Creating the Environment

1. Open VSCode and open the terminal (View > Terminal or Ctrl+`)

2. Create a new virtual environment named "hackbot":
```bash
python -m venv hackbot
```

3. Activate the virtual environment:
```bash
.\hackbot\Scripts\activate
```

##### Installing Required Packages

4. Install Selenium and WebDriver Manager:
```bash
pip install selenium webdriver-manager
```

5. Create a requirements.txt file to track dependencies:
```bash
pip freeze > requirements.txt
```

##### Setting as Default Environment

6. Set as default interpreter in VSCode:
   - Press `Ctrl+Shift+P` to open command palette
   - Type "Python: Select Interpreter"
   - Choose the interpreter at `hackbot/Scripts/python.exe`

##### Verification

7. Verify the environment is active:
   - Look for "(hackbot)" at the start of your terminal prompt
   - Check VSCode status bar shows "hackbot" as selected Python interpreter

##### Common Commands

- Deactivate the environment:
```bash
deactivate
```

- Install packages from requirements.txt:
```bash
pip install -r requirements.txt
```

- Update pip in the environment:
```bash
python -m pip install --upgrade pip
```