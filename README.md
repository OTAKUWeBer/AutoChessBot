# Chess Position Evaluator

This project captures a chessboard from a screenshot, extracts its FEN (Forsyth–Edwards Notation) representation, and uses Stockfish to suggest the best move. It also includes plans for a graphical user interface (GUI).

## Features
✅ Captures the chessboard image using a double-click  
✅ Extracts the FEN from the image via [Chessify](https://chessify.me)  
✅ Automatically flips the board if playing as Black  
✅ Uses Stockfish to suggest the best move  
✅ **Auto Move Execution**: Automatically makes the best move in the game  
🛠 **Upcoming Features:**  
  - **Graphical User Interface (GUI)**: A user-friendly interface instead of the terminal  

## Prerequisites
Ensure you have the following installed:

- Python 3.10+
- `requests` (`pip install requests`)
- `pynput` (`pip install pynput`)
- `mss` (`pip install mss`)
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
sudo pacman -S stockfish   # Arch Linux
sudo dnf install stockfish  # Fedora
```

### Windows Users
Download `stockfish.exe` from [Stockfish](https://stockfishchess.org/download/) and place it in the **same directory** as `main.py` (AutoChessBot).

## Usage
1. **Run the script:**  
   ```bash
   python main.py
   ```  

2. **Choose your color when prompted:**  
   - Enter `1` if playing as White  
   - Enter `2` if playing as Black  

3. **Use 90% zoom for better accuracy.**  

4. **Double-click on the chessboard or anywhere after opening Chess.com in your game for auto best move.**  

5. The script will:  
   - Extract the FEN  
   - Flip the board if necessary  
   - Get the best move from Stockfish  
   - Automatically execute the best move in your game  

6. The best move will be displayed in the terminal.  

### (Planned) Graphical User Interface
A GUI will replace the terminal-based interaction, making the tool more user-friendly.

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

