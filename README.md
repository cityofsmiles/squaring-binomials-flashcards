# Squaring Binomials Flashcards

This project is an interactive flashcards web app designed to help high
school algebra students practice **squaring binomials**. It uses a
Python backend to generate the math problems and a React frontend to
provide a smooth, animated flashcard experience.

## Project Structure

-   **Backend (Python)**\
    The backend uses [Sympy](https://www.sympy.org/) to generate
    binomial expressions and their expanded forms.
    -   Generates 200 flashcards (50 for each case).\
    -   Each flashcard has a question (the binomial squared) and the
        correct simplified answer.\
    -   The flashcards are exported as `public/flashcards.json` for the
        React app.
-   **Frontend (React)**\
    The React app loads the pre-generated flashcards, randomly selects
    10 per session, and provides:
    -   Animated flashcards with flip and reveal effects.\
    -   Input fields for student answers.\
    -   Automatic answer checking against the JSON.\
    -   Score tracking and answer key review.

## Covered Cases

The flashcards cover four types of binomial squaring patterns:

1.  **Case 1:** \\((x Â± b)\^2 = x\^2 Â± 2bx + b\^2\\)\
    Example: \\((x - 2)\^2 = x\^2 - 4x + 4\\)

2.  **Case 2:** \\((x Â± by)\^2 = x\^2 Â± 2bxy + b^2y^2\\)\
    Example: \\((x + 4y)\^2 = x\^2 + 8xy + 16y\^2\\)

3.  **Case 3:** \\((ax Â± b)\^2 = a^2x^2 Â± 2abx + b\^2\\)\
    Example: \\((3x - 2)\^2 = 9x\^2 - 12x + 4\\)

4.  **Case 4:** \\((ax Â± by)\^2 = a^2x^2 Â± 2abxy + b^2y^2\\)\
    Example: \\((3x - 2y)\^2 = 9x\^2 - 12xy + 4y\^2\\)

## Installation and Setup

### Backend (Flashcard Generation)

1.  Clone this repository:

    ``` bash
    git clone https://github.com/cityofsmiles/squaring-binomials-flashcards.git
    cd squaring-binomials-flashcards
    ```

2.  Create a virtual environment and install dependencies:

    ``` bash
    python -m venv venv
    source venv/bin/activate   # macOS/Linux
    venv\Scripts\activate    # Windows
    pip install sympy
    ```

3.  Run the generator script:

    ``` bash
    python generate_flashcards.py
    ```

    This creates `public/flashcards.json` with 200 flashcards.

### Frontend (React App)

1.  Install dependencies:

    ``` bash
    npm install
    ```

2.  Run the development server:

    ``` bash
    npm start
    ```

3.  Open your browser at `http://localhost:3000`.

## Deployment

This app is deployed using GitHub Pages at:\
<https://cityofsmiles.github.io/squaring-binomials-flashcards>

To deploy updates:

``` bash
npm run build
npm run deploy
```

## License

This project is licensed under the MIT License.