// Firebase configuration
// Firebase is Google's platform for authentication and database

import { initializeApp } from 'firebase/app';
import { getAuth } from 'firebase/auth';
import { getFirestore } from 'firebase/firestore';

// Your Firebase project configuration
// You'll need to create a Firebase project at: https://console.firebase.google.com/
// For now, these are placeholder values - we'll add real ones later

const firebaseConfig = {
  apiKey: "YOUR_API_KEY",
  authDomain: "YOUR_PROJECT_ID.firebaseapp.com",
  projectId: "YOUR_PROJECT_ID",
  storageBucket: "YOUR_PROJECT_ID.appspot.com",
  messagingSenderId: "YOUR_MESSAGING_SENDER_ID",
  appId: "YOUR_APP_ID"
};

// Initialize Firebase
const app = initializeApp(firebaseConfig);

// Get authentication service
// This handles login, signup, etc.
export const auth = getAuth(app);

// Get Firestore database
// This is where we'll store student and faculty data
export const db = getFirestore(app);
