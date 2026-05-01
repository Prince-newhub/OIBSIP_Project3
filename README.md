# OIBSIP_Project2

# Random Password Generator 🔐

A feature-rich, graphical password generator built with Python and Tkinter. Create strong, customizable passwords with an intuitive GUI interface.

## Features ✨

- **Customizable length** - Generate passwords from 4+ characters
- **Character type selection** - Choose from:
  - Uppercase letters (A-Z)
  - Lowercase letters (a-z)
  - Numbers (0-9)
  - Symbols (!"#$%&'()*+,-./:;<=>?@[\]^_`{|}~)
- **Character exclusion** - Exclude specific characters you don't want
- **Real-time preview** - See which character types are selected
- **Copy to clipboard** - One-click copy functionality
- **Modern dark theme** - Easy on the eyes

## Requirements 📋

- Python 3.x
- Required packages:
  ```bash
  pip install pyperclip
  ```

## Installation 🚀

1. **Clone or download** this script to your computer

2. **Install dependencies**:
   ```bash
   pip install pyperclip
   ```
   > Note: `tkinter` comes pre-installed with most Python distributions

3. **Run the application**:
   ```bash
   python password_generator.py
   ```

## How to Use 🎮

1. **Set password length** - Enter a number (minimum 4)
2. **Select character types** - Check/uncheck the boxes as needed
3. **Exclude characters** (optional) - Enter any characters you want to avoid
4. **Click "Generate Password"** - Your password appears in the box
5. **Click "Copy to Clipboard"** - Password is ready to paste anywhere

## Example Usage 💡

```
Length: 16
Selected: Uppercase, Lowercase, Numbers, Symbols
Exclude: O0l1 (for better readability)
Generated: Xy#9Km$2Pq@8Wn&5
```

## Screenshot Preview 📸

```
┌─────────────────────────────────┐
│     Password Generator          │
├─────────────────────────────────┤
│  Password Length: [12      ]    │
│                                  │
│  ☑ Uppercase                     │
│  ☑ Lowercase                     │
│  ☑ Numbers                       │
│  ☑ Symbols                       │
│                                  │
│  Selected: Uppercase, Lowercase  │
│           Numbers, Symbols       │
│                                  │
│  Exclude: [            ]         │
│                                  │
│  [     aB3$xK9&Qw     ]          │
│                                  │
│  [ Generate Password ]           │
│  [ Copy to Clipboard ]           │
└─────────────────────────────────┘
```

## Error Handling ⚠️

The application handles these scenarios gracefully:
- Invalid/empty length input
- Length less than 4 characters
- No character types selected
- All characters excluded (empty character set)
- No password to copy

## Customization 🎨

You can easily modify:
- Window size (change `geometry()` parameters)
- Color scheme (modify `bg`, `fg` values)
- Default length (change `StringVar(value="12")`)
- Default selections (modify `BooleanVar(value=True/False)`)

## License 📄

Free to use, modify, and distribute.

---

