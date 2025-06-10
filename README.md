# Spin The Wheel Game

## Overview

1. Spin The Wheel Game is an interactive Pygame application where players spin a wheel to answer a series of questions based on a customizable universe. The game features a configuration screen to set up the universe, background, music, and number of answers per question. Results are displayed with optional GIF animations and random responses, providing a fun and engaging experience.

## Features

- **Customizable Universe**: Define a universe (e.g., "Star Wars") to generate themed answers via OpenAI API.
- **Dynamic Wheel**: Spin a wheel with a variable number of segments (4-8) for each question.
- **GIF Animations**: Displays GIFs corresponding to wheel results for visual feedback.
- **Configuration Screen**: Adjust background color, image, music file, and number of answers per question.
- **Results Saving**: Save final results as an image and view detailed outcomes.
- **Random Responses**: Unique responses are generated for each result, enhancing replayability.

## Requirements

The game requires Python and the following dependencies (listed in the provided setup):

- **Python Packages**:
  - annotated-types==0.7.0
  - anyio==4.9.0
  - certifi==2025.4.26
  - distro==1.9.0
  - h11==0.16.0
  - httpcore==1.0.9
  - httpx==0.28.1
  - idna==3.10
  - imageio==2.37.0
  - jiter==0.9.0
  - numpy==2.2.4
  - openai==1.78.1
  - pillow==11.2.1
  - pydantic==2.11.4
  - pydantic_core==2.33.2
  - pygame==2.6.1
  - sniffio==1.3.1
  - tqdm==4.67.1
  - typing-inspection==0.4.0
  - typing_extensions==4.13.2

## Installation

1. **Clone the Repository**:

   ```bash
   git clone <repository-url>
   cd <repository-directory>
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
4. **Prepare Assets**:
   - Place background images in `assets/backgrounds/`.
   - Place sound files (e.g., `spin.mp3`) in `assets/sfx/`.
   - Place GIF files (named after wheel results, e.g., `1.1.gif`) in `assets/gifs/`.
   - Ensure `TextResp.json` is available for random responses.
   - Ensure `config.json` is writable for saving configurations.

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
   - Click "Zapisz wynik" to save the results as `result.png`.
   - Click "Zakończ" to exit the game.

## File Structure

- `main.py`: Entry point, manages game states (menu, config, game).
- `app.py`: Core game logic for spinning the wheel, displaying GIFs, and showing results.
- `spin_wheel.py`: Handles wheel mechanics, spinning, and segment selection.
- `menu.py`: Displays the main menu with options to configure or play.
- `config.py`: Configuration screen for customizing game settings and generating AI answers.
- `constants.py`: Defines constants like window size, colors, and questions.
- `gpt.py`: Integrates OpenAI API for generating themed answers.
- `assets/`:
  - `backgrounds/`: Background images (e.g., `bg.png`).
  - `sfx/`: Sound files (e.g., `spin.mp3`).
  - `gifs/`: GIFs for results (e.g., `1.1.gif`).
- `config.json`: Stores game configuration.
- `TextResp.json`: Contains random responses for each draw and result.

## Configuration

- **Universe**: Enter a theme (e.g., "Star Wars") for AI-generated answers.
- **Background Color**: Choose from predefined colors via the color picker.
- **Background Image**: Specify a file name (e.g., `bg.png`) in `assets/backgrounds/`.
- **Music File**: Specify a file name (e.g., `music.mp3`) in `assets/backgrounds/`.
- **Number of Answers**: Set the number of wheel segments (numeric input) for each question.
- Save and generate AI answers by clicking "Zapisz i Generuj", or return to the menu with "Powrót".

## Notes

- **GIF Support**: Ensure GIF files match the format `<question_number>.<result_index>.gif` (e.g., `1.1.gif`).
- **Error Handling**: If a GIF or asset is missing, the game continues without it and logs an error.
- **AI Integration**: Requires an active OpenAI API key for generating answers.
- **Performance**: Runs at 60 FPS, with smooth wheel spinning and GIF animation.

## Troubleshooting

- **Missing Assets**: Check that all files (GIFs, music, backgrounds) are in the correct `assets/` subdirectories.
- **API Errors**: Verify your OpenAI API key and internet connection.
- **Dependency Issues**: Ensure all packages are installed correctly via `pip`.

## License

This project is for personal use and demonstration. Ensure compliance with OpenAI’s API terms and any asset licensing (e.g., music, images, GIFs).