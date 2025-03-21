import React, { useState } from "react";
import API from "./axios.js";

const GameHandler = () => {
    const [gameId, setGameId] = useState(null);
    const [loading, setLoading] = useState(false);
    const [responseData, setResponseData] = useState(null);

    const startGame = async () => {
        setLoading(true);
        try {
            const response = await API.post();
            if (response.status === 201) {
                setGameId(response.data.id);
                setResponseData(response.data);
                console.log("Game Created:", response.data);
            } else {
                console.error("Failed to create game:", response.status);
            }
        } catch (error) {
            console.error("Error creating game:", error);
        }
        setLoading(false);
    };

    return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-gradient-to-r from-blue-500 to-purple-600 text-white">
            {gameId ? (
                <div className="bg-white text-gray-800 p-8 rounded-lg shadow-lg w-96">
                    <h1 className="text-2xl font-bold text-center mb-4">Game Started!</h1>
                    <p className="text-center text-lg mb-4">
                        <span className="font-semibold">Game ID:</span> {gameId}
                    </p>
                    <div className="mb-4">
                        <h2 className="text-xl font-semibold mb-2">Player Hand:</h2>
                        <ul className="list-disc list-inside">
                            <li>
                                {responseData.player_hand[0].value} of {responseData.player_hand[0].suit}
                            </li>
                            <li>
                                {responseData.player_hand[1].value} of {responseData.player_hand[1].suit}
                            </li>
                        </ul>
                    </div>
                    <p className="text-lg">
                        <span className="font-semibold">Player Score:</span> {responseData.player_score}
                    </p>
                </div>
            ) : (
                <div className="text-center">
                    <h1 className="text-4xl font-bold mb-6">Ready to Play Blackjack?</h1>
                    <button
                        onClick={startGame}
                        className="px-6 py-3 bg-green-500 text-white text-lg font-semibold rounded-lg shadow-lg hover:bg-green-600 transition duration-300"
                        disabled={loading}
                    >
                        {loading ? "Starting..." : "Start Game"}
                    </button>
                </div>
            )}
        </div>
    );
};

export default GameHandler;