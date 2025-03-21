import React, { useEffect, useState } from "react";
import API from "./axios.js";


const GameHandler = () => {
    const [gameId, setGameId] = useState(null);
    const [loading, setLoading] = useState(false);

    const startGame = async () => {
        setLoading(true);
        // Sent a POST request to create a game
        const response = await API.post();
        console.log(response);  
        if (response.status === 201) {
            setGameId(response.data.id); // Assuming the response contains the game ID
            console.log("Game Created:", response.data);
        } else {
            console.error("Failed to create game:", response.status);
        }
        setLoading(false);

    };

    return (
        <div className="flex flex-col items-center justify-center min-h-screen bg-gray-100">
            {gameId ? (
                <div>
                    <h1 className="text-2xl font-bold">Game ID: {gameId}</h1>
                    <p>Your game has been created! Access it via ID: {gameId}</p>
                </div>
            ) : (
                <div>
                    <h1 className="text-3xl font-bold mb-4">Start Game?</h1>
                    <button
                        onClick={startGame}
                        className="px-4 py-2 bg-blue-500 text-white rounded-lg hover:bg-blue-700"
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
