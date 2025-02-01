# Chess Position Evaluator

This project captures a chessboard from a screenshot, extracts its FEN (Forsyth–Edwards Notation) representation, and uses Stockfish to suggest the best move.

## Features
- Captures the chessboard image using a double-click
- Extracts the FEN from the image via [Chessify](https://chessify.me)
- Automatically flips the board if playing as Black
- Uses Stockfish to suggest the best move

## Prerequisites
Ensure you have the following installed:

- Python 12+
- `requests` (`pip install requests`)
- `pynput` (`pip install pynput`)
- `mss` (`pip install mss`) (For X11-based systems)
- `grim` (For Wayland-based systems, install via package manager)
- Stockfish chess engine ([Download here](https://stockfishchess.org/))

## Installation
```bash
git clone https://github.com/OTAKUWeBer/AutoChessBot.git
cd AutoChessBot
pip install -r requirements.txt 
```

```bash
# If you use Wayland (e.g., Sway, Hyprland):
sudo pacman -S grim
```

## Usage
1. **Run the script:**
   ```bash
   python main.py
   ```

2. **Choose your color when prompted:**
   - Enter `1` if playing as White
   - Enter `2` if playing as Black

3. **Double-click on the chessboard in your game to capture a screenshot.**

4. The script will:
   - Extract the FEN
   - Flip the board if necessary
   - Get the best move from Stockfish

5. The best move will be displayed in the terminal.

## Configuration
You need to provide a session ID for Chessify in `getfen.py`:
```python
cookies = {
    "session_id": "your_chessify_session_id_here"
}
```

## License
This project is licensed under the MIT License.

## Contributing
Pull requests are welcome! Feel free to open an issue if you have any suggestions or improvements.


