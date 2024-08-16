# Pomodoro Timer

![Pomodoro Timer Logo](public/logo.png)

## Overview

Pomodoro Timer is a web application designed to help you manage your time effectively using the Pomodoro Technique. This app allows you to customize work sessions and break intervals, track Pomodoro cycles, and view session history. It features a modern UI with a 16-bit style tomato clock logo, customizable settings, and a continuous timer that keeps running even when the browser tab is inactive.

**Note:** The app is also a Progressive Web App (PWA), which means it can be installed and run on mobile devices when hosted on a remote domain.

## Features

- **Customizable Timer Durations**: Set custom durations for work sessions and breaks.
- **Pomodoro Cycles**: Configure the number of cycles before a long break and set long break durations.
- **Session History**: Track and view the history of completed sessions with pagination and sorting by most recent.
- **Notifications**: Get notified when a session or break ends.
- **Progressive Web App (PWA)**: Install the app on mobile devices and run it offline.
- **User-Friendly UI**: Easy-to-use interface with collapsible settings panel and dynamic updates.
- **Continuous Timer**: Timer continues to count down even when the browser tab is not in focus.

## Installation

To run the Pomodoro Timer app locally, follow these steps:

### Prerequisites

- Node.js (version 12 or higher)
- npm (Node Package Manager)

### Clone the Repository

```bash
git clone https://github.com/jwalker/pomodoro-timer.git
cd pomodoro-timer
```

### Run the backend

```bash
cd backend
uv venv
source .venv
uv pip install -r requirements.txt
python app.py
```

## Install Frontend

```bash
cd frontend
```

### Install Dependencies

```bash
npm install
```

### Run the Development Server

```bash
npm run serve
```

### Build for Production

```bash
npm run build
```

## Usage

- Start a Session: Set your desired session name, duration, and break intervals in the settings panel. Press the "Play" button to start the timer.
- Pause/Stop a Session: Use the "Stop" button to pause or stop the current session.
- Reset the Timer: Reset the timer to your default settings with the "Reset" button.
- Track Progress: View completed session history with pagination and sorting by most recent.

## Progressive Web App (PWA)

### Installation on Mobile Devices

When hosted on a remote domain, the Pomodoro Timer app can be installed as a PWA on mobile devices. This allows you to access the app offline and run it as if it were a native app.

- Visit the App URL: Navigate to the app’s URL in your mobile browser.
- Install the App: Look for the "Add to Home Screen" option in your browser settings (usually under the browser's menu).
- Run Offline: Once installed, you can run the app directly from your home screen, even without an internet connection.

Contact
For questions or feedback, please contact me via [GitHub](https://github.com/jwalker) and [X](https://x.com/call_eax)