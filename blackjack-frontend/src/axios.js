// src/api/axios.js
import axios from "axios";

const API = axios.create({
  baseURL: "http://http://127.0.0.1:8000/api/game/", // Replace with your Django REST Framework base URL
  timeout: 5000, // Optional timeout in milliseconds
  headers: {
    "Content-Type": "application/json",
  },
});

export default API;
