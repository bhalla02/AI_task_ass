import pyttsx3

engine = pyttsx3.init()

tests = {
    "algebra_question.wav": "Solve x square minus five x plus six equals zero.",
    "probability_question.wav": "A fair coin is tossed twice. What is the probability of getting two heads?",
    "ambiguous_question.wav": "Solve x square plus three x."
}

for filename, text in tests.items():
    engine.save_to_file(text, filename)

engine.runAndWait()

print("Audio test files generated.")