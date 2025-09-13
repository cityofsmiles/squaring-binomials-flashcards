

import React, { useState, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { parse, simplify } from "mathjs";
import "./flashcards.css";

export default function App() {
  const [flashcards, setFlashcards] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [answers, setAnswers] = useState({});
  const [showResults, setShowResults] = useState(false);
  const [loading, setLoading] = useState(true);

  // Normalize user input (lowercase, remove spaces)
  const normalize = (str) =>
    str.replace(/\s+/g, "").toLowerCase();

  // Format expression for display
  const formatExpr = (exprStr) => {
    try {
      return simplify(parse(normalize(exprStr))).toString();
    } catch {
      return exprStr || "(none)";
    }
  };

  // Check correctness algebraically
  const checkAnswer = (userInput, correctAnswer) => {
    try {
      const userExpr = simplify(parse(normalize(userInput)));
      const correctExpr = simplify(parse(normalize(correctAnswer)));
      return simplify(userExpr.subtract(correctExpr)).equals(0);
    } catch {
      return false;
    }
  };

  // Load flashcards JSON
  const loadFlashcards = () => {
    const base =
      import.meta.env.MODE === "development"
        ? "/flashcards.json"
        : "https://cityofsmiles.github.io/squaring-binomials-flashcards/flashcards.json";

    fetch(base)
      .then((res) => res.json())
      .then((data) => {
        const shuffled = data.sort(() => 0.5 - Math.random()).slice(0, 10);
        setFlashcards(shuffled);
        setCurrentIndex(0);
        setAnswers({});
        setShowResults(false);
        setLoading(false);
      });
  };

  useEffect(() => {
    loadFlashcards();
  }, []);

  const handleAnswer = (value) =>
    setAnswers({ ...answers, [currentIndex]: value });

  const nextCard = () =>
    setCurrentIndex((prev) =>
      prev === flashcards.length - 1 ? prev : prev + 1
    );

  const prevCard = () =>
    setCurrentIndex((prev) => (prev === 0 ? prev : prev - 1));

  if (loading) return <p>Loading flashcards...</p>;

  if (showResults) {
    const score = flashcards.filter((card, i) =>
      checkAnswer(answers[i] || "", card.answer)
    ).length;

    return (
      <motion.div
        className="answer-key-screen"
        initial={{ opacity: 0, y: 30 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
      >
        <h1 className="score">
          Score: {score}/{flashcards.length}
        </h1>
        <h3 style={{ marginBottom: "1rem", color: "#555" }}>Answer Key</h3>

        <div className="answer-key">
          {flashcards.map((card, i) => {
            const correct = checkAnswer(answers[i] || "", card.answer);
            return (
              <motion.div
                key={i}
                className={`answer-item ${correct ? "correct-bg" : "incorrect-bg"}`}
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: i * 0.05 }}
              >
                <p>
                  <strong>Q{i + 1}:</strong> {card.question} <br />
                  Your Answer: {formatExpr(answers[i])}{" "}
                  <span className={correct ? "correct" : "incorrect"}>
                    {correct ? "✓" : "✗"}
                  </span>
                  <br />
                  Correct Answer: {formatExpr(card.answer)}
                </p>
              </motion.div>
            );
          })}
        </div>

        <div className="button-group">
          <button className="btn-primary" onClick={loadFlashcards}>
            Try Another Set
          </button>
          <button className="btn-submit" onClick={() => setShowResults(false)}>
            Back to Cards
          </button>
        </div>
      </motion.div>
    );
  }

  const currentCard = flashcards[currentIndex];

  return (
    <div className="flashcards-container">
      <h1>Squaring Binomials Flashcards</h1>
      <h3 style={{ fontWeight: "normal", marginBottom: "1rem" }}>
        by Jonathan R. Bacolod, LPT
      </h3>
      <h2>
        Flashcard {currentIndex + 1} of {flashcards.length}
      </h2>

      <div className="flashcard-container">
        <AnimatePresence mode="wait">
          <motion.div
            key={currentIndex}
            className="flashcard"
            initial={{ opacity: 0, x: 50 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -50 }}
            transition={{ duration: 0.3 }}
          >
            {currentCard.question}
          </motion.div>
        </AnimatePresence>
      </div>

      <input
        type="text"
        className="input-answer"
        placeholder="Your answer"
        value={answers[currentIndex] || ""}
        onChange={(e) => handleAnswer(e.target.value)}
      />

      <div className="button-group">
        <button className="btn-primary" onClick={prevCard} disabled={currentIndex === 0}>
          Previous
        </button>
        <button
          className="btn-primary"
          onClick={nextCard}
          disabled={currentIndex === flashcards.length - 1}
        >
          Next
        </button>
        <button className="btn-submit" onClick={() => setShowResults(true)}>
          Submit
        </button>
      </div>
    </div>
  );
}




