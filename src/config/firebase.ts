// Firebase configuration
// Firebase is Google's platform for authentication and database

import { initializeApp } from 'firebase/app';
import { getAuth } from 'firebase/auth';
import { getFirestore } from 'firebase/firestore';

// Your Firebase project configuration
// You'll need to create a Firebase project at: https://console.firebase.google.com/
// For now, these are placeholder values - we'll add real ones later

const firebaseConfig = {
  apiKey: "AIzaSyCANsFgc8ol6YT_QD7BXRUHu0y2-L0Z2wU",
  authDomain: "siblings-110dd.firebaseapp.com",
  projectId: "siblings-110dd",
  storageBucket: "siblings-110dd.firebasestorage.app",
  messagingSenderId: "771796793386",
  appId: "1:771796793386:web:5165e14fc573315ecf6b53",
  measurementId: "G-2ZGKSHBSVC"
};



// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Get authentication service
// This handles login, signup, etc.
export const auth = getAuth(app);

// Get Firestore database
// This is where we'll store student and faculty data
export const db = getFirestore(app);
