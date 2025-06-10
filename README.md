# Spin The Wheel Game

#### Spin The Wheel Game is an interactive Pygame application where players spin a wheel to answer a series of questions based on a customizable universe.
The game features a configuration screen to set up the universe, background, music, and number of answers per question.
Results are displayed with optional GIF animations and random responses, providing a fun and engaging experience.

## Features

- **Customizable Universe**: Define a universe (e.g., "Star Wars") to generate themed answers via OpenAI API.
- **Dynamic Wheel**: Spin a wheel with a variable number of segments (4-8) for each question.
- **GIF Animations**: Displays GIFs corresponding to wheel results for visual feedback.
- **Configuration Screen**: Adjust background color, image, music file, and number of answers per question.
- **Results Saving**: Save final results as an image and view detailed outcomes.
- **Random Responses**: Unique responses are generated for each result, enhancing replayability.

## Requirements

The game requires Python and the dependencies listed in the requirements.txt file.

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/MalarzDawid/KFT.git
   cd KFT
   ```
2. **Install Dependencies**: Create a virtual environment and install the required packages:

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```
   
3. **Set Up OpenAI API**:
   - Obtain an API key from OpenAI.
   - Replace the empty string in `client = OpenAI(api_key="")` in the code with your API key.

## How to Play

1. **Launch the Game**:

   ```bash
   python main.py
   ```
2. **Menu**:
   - **Configure Game**: Customize the universe, background color, image, music, and number of answers.
   - **Play Game**: Start spinning the wheel to answer questions.
3. **Gameplay**:
   - Press `SPACE` or click to spin the wheel.
   - The wheel stops on a result, optionally displaying a GIF and a random response.
   - After a short delay, the next question’s wheel is generated.
4. **Results**:
   - View all results and responses at the end.
   - Click "Save" to save the results as `result.png`.
   - Click "Exit" to exit the game.

## License

This project is for personal use and demonstration.