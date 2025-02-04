# Chess Position Evaluator

This project captures a chessboard from a screenshot, extracts its FEN (Forsyth–Edwards Notation) representation, and uses Stockfish to suggest the best move. It now includes a graphical user interface (GUI) using Tkinter.

## Features
✅ Captures the chessboard image using a single click  
✅ Extracts the FEN from the image via [Chessify](https://chessify.me)  
✅ Automatically flips the board if playing as Black  
✅ Uses Stockfish to suggest the best move  
✅ **Auto Move Execution**: Automatically makes the best move in the game  
✅ **Graphical User Interface (GUI)**: A user-friendly interface instead of the terminal  
🛠 **New Features:**  
  - **ESC to go back and choose color again**  

## Prerequisites
Ensure you have the following installed:

- Python 3.10+
- `requests` (`pip install requests`)
- `mss` (`pip install mss`)
- `opencv` (`pip install opencv-python`)
- `pyautogui` (`pip install pyautogui`)
- `tkinter` (Pre-installed with Python)
- Stockfish chess engine ([Download here](https://stockfishchess.org/))

## Installation
```bash
git clone https://github.com/OTAKUWeBer/AutoChessBot.git
cd AutoChessBot
pip install -r requirements.txt
```

### Linux Users
To install Stockfish on Linux:
```bash
sudo apt install stockfish  # Debian/Ubuntu
paru/yay -S stockfish   # Arch Linux
sudo dnf install stockfish  # Fedora
```

### Windows Users
Download `stockfish.exe` from [Stockfish](https://stockfishchess.org/download/) and place it in the **same directory** as `main.py` (AutoChessBot).

## Usage
1. **Run the script:**  
   ```bash
   python main.py
   ```  

2. **Choose your color using the GUI:**  
   - Click `White` if playing as White  
   - Click `Black` if playing as Black  
   - Press `ESC` to go back and choose the color again  

3. **Use 100% zoom for better accuracy.**   

4. The script will: (After you click "Play next move")
   - Extract the FEN  
   - Flip the board if necessary  
   - Get the best move from Stockfish  
   - Automatically execute the best move in your game  

5. The best move will be displayed only in the GUI.  

6. **For better visibility, move the Tkinter application window to the side so the board is clearly visible.**  

## Configuration
You need to provide a session ID for Chessify in `getfen.py`:
```python
cookies = {
    "session_id": "your_chessify_session_id_here"
}
```

## Disclaimer
⚠️ **Using this tool for online chess games may result in bans. Use at your own risk.**

## License
This project is licensed under the MIT License.

## Contributing
Pull requests are welcome! Feel free to open an issue if you have any suggestions or improvements.

## Acknowledgments
* [Zai-Kun (For creating the wrapper around chessify.me)](https://github.com/Zai-Kun)