<template>
  <div id="app" class="app-container">
    <!-- Left Sidebar -->
    <aside class="sidebar">
      <!-- Logo Section -->
      <div class="logo-container">
        <img src="/logo.png" width="250" height="250" alt="Pomodoro Timer Logo" class="logo" />
      </div>
      
      <button @click="toggleSettings" class="toggle-button">
        {{ settingsVisible ? 'Hide Settings' : 'Show Settings' }}
      </button>
      <transition name="slide-fade">
        <div v-if="settingsVisible" class="session-input">
          <h2>Settings</h2>
          <label for="session-name">Session Name:</label>
          <input v-model="sessionName" id="session-name" placeholder="Enter session name" />

          <label for="session-duration">Session Duration:</label>
          <select v-model="sessionDuration" id="session-duration" @change="updateSessionInfo">
            <option value="25">25 minutes</option>
            <option value="30">30 minutes</option>
            <option value="40">40 minutes</option>
          </select>

          <label for="break-duration">Break Duration:</label>
          <select v-model="breakDuration" id="break-duration" @change="updateSessionInfo">
            <option value="5">5 minutes</option>
            <option value="15">15 minutes</option>
            <option value="30">30 minutes</option>
          </select>

          <!-- Pomodoro Cycle Settings -->
          <label for="cycle-count">Number of Cycles:</label>
          <select v-model="cycleCount" id="cycle-count">
            <option value="3">3 cycles</option>
            <option value="4">4 cycles</option>
            <option value="5">5 cycles</option>
          </select>

          <label for="long-break-duration">Long Break Duration:</label>
          <select v-model="longBreakDuration" id="long-break-duration">
            <option value="10">10 minutes</option>
            <option value="15">15 minutes</option>
            <option value="20">20 minutes</option>
            <option value="30">30 minutes</option>
            <option value="40">40 minutes</option>
          </select>
        </div>
      </transition>
    </aside>

    <!-- Main Timer Section -->
    <main class="main-content">
      <div class="timer">
        <h1>{{ formattedTime }}</h1>
        <div class="button-group">
          <button @click="startTimer">
            <i class="fas fa-play"></i>
          </button>
          <button @click="stopTimer">
            <i class="fas fa-stop"></i>
          </button>
          <button @click="resetTimer">
            <i class="fas fa-redo"></i>
          </button>
        </div>
      </div>
      <div class="history">
        <h2>Session History</h2>
        <ul>
          <li v-for="session in paginatedHistory" :key="session.start_time">
            <strong>{{ session.name }}</strong> - {{ session.start_time }}
          </li>
        </ul>
        <div class="pagination">
          <button @click="prevPage" :disabled="currentPage === 1">Previous</button>
          <button @click="nextPage" :disabled="currentPage === totalPages">Next</button>
        </div>
      </div>
      <!-- Footer with Author Info -->
      <footer class="footer">
        <p>Made with <span class="tomatoe">🍅</span> in California by Jacolon Walker</p>
        <div class="social-links" align="center" >
          <a href="https://github.com/jwalker" target="_blank" aria-label="GitHub">
            <i class="fab fa-github"></i>
          </a>
          <a href="https://x.com/call_eax" target="_blank" aria-label="X">
            <i class="fab fa-x-twitter"></i>
          </a>
        </div>
      </footer>
      <audio id="bell-sound" src="/metal_gong.mp3"></audio>
    </main>
  </div>
</template>

<script>
export default {
  data() {
    return {
      timer: null,
      timerRunning: false,
      timeLeft: 25 * 60,
      sessionName: '',
      sessionDuration: 25,
      breakDuration: 5,
      sessionHistory: [],
      cycleCount: 4,          // Number of cycles before a long break
      longBreakDuration: 15,  // Duration of the long break in minutes
      currentCycle: 1,         // Current cycle number
      settingsVisible: false, // State to control visibility of settings
      currentPage: 1,         // Current page for session history
      sessionsPerPage: 5      // Number of sessions to display per page
    };
  },
  computed: {
    formattedTime() {
      const minutes = Math.floor(this.timeLeft / 60);
      const seconds = this.timeLeft % 60;
      return `${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
    },
    sortedSessionHistory() {
      return [...this.sessionHistory].sort((a, b) => new Date(b.start_time) - new Date(a.start_time));
    },
    paginatedHistory() {
      const start = (this.currentPage - 1) * this.sessionsPerPage;
      const end = start + this.sessionsPerPage;
      return this.sortedSessionHistory.slice(start, end);
    },
    totalPages() {
      return Math.ceil(this.sortedSessionHistory.length / this.sessionsPerPage);
    }
  },
  methods: {
    toggleSettings() {
      this.settingsVisible = !this.settingsVisible;
    },
    updateSessionInfo() {
      this.timeLeft = this.sessionDuration * 60;
    },
    startTimer() {
      if (this.timerRunning) return;

      this.timerRunning = true;
      const startTime = Date.now();
      const targetTime = startTime + this.timeLeft * 1000; // End time in milliseconds

      this.timer = setInterval(() => {
        const currentTime = Date.now();
        this.timeLeft = Math.max(0, Math.ceil((targetTime - currentTime) / 1000));

        if (this.timeLeft <= 0) {
          clearInterval(this.timer);
          this.playBellSound();
          alert("Time's up! Take a break.");
          this.timerRunning = false;
          this.completeSession();
        }
      }, 1000);

      fetch('http://127.0.0.1:5000/api/start_timer', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          duration: this.timeLeft,
          session_name: this.sessionName || 'Unnamed Session'
        })
      })
        .then(response => response.json())
        .then(data => {
          if (data.message === "Timer started") {
            this.sessionHistory.push({
              name: this.sessionName || 'Unnamed Session',
              start_time: new Date().toLocaleString()
            });
          } else {
            console.error('Failed to start timer:', data.message);
          }
        })
        .catch(error => {
          console.error('Error:', error);
          alert('Failed to start the timer. Please check the network or server configuration.');
        });
    },
    completeSession() {
      alert("Session complete!");
      this.currentCycle++;
      if (this.currentCycle > this.cycleCount) {
        this.currentCycle = 1;
        this.timeLeft = this.longBreakDuration * 60;
        alert("Long break! Relax for a while.");
      } else {
        this.startBreakTimer();
      }
    },
    startBreakTimer() {
      this.timeLeft = this.breakDuration * 60;
      this.timerRunning = true;
      const startTime = Date.now();
      const targetTime = startTime + this.timeLeft * 1000;

      this.timer = setInterval(() => {
        const currentTime = Date.now();
        this.timeLeft = Math.max(0, Math.ceil((targetTime - currentTime) / 1000));

        if (this.timeLeft <= 0) {
          clearInterval(this.timer);
          this.playBellSound();
          alert('Break over! Time to get back to work.');
          this.timerRunning = false;
        }
      }, 1000);
    },
    stopTimer() {
      clearInterval(this.timer);
      this.timerRunning = false;
      fetch('http://127.0.0.1:5000/api/stop_timer', {
        method: 'POST'
      });
    },
    resetTimer() {
      clearInterval(this.timer);
      this.timerRunning = false;
      this.updateSessionInfo();
      this.currentCycle = 1; // Reset cycle count on reset
      fetch('http://127.0.0.1:5000/api/reset_timer', {
        method: 'POST'
      });
    },
    playBellSound() {
      const bellSound = document.getElementById('bell-sound');
      bellSound.play();
    },
    nextPage() {
      if (this.currentPage < this.totalPages) {
        this.currentPage++;
      }
    },
    prevPage() {
      if (this.currentPage > 1) {
        this.currentPage--;
      }
    }
  },
  created() {
    this.updateSessionInfo();
    fetch('http://127.0.0.1:5000/api/get_history')
      .then(response => response.json())
      .then(data => {
        this.sessionHistory = data;
      });
  }
};
</script>

<style>
/* Global Styles */
body {
  font-family: 'Arial', sans-serif;
  margin: 0;
  background-color: #f0f0f0;
}

.app-container {
  display: flex;
  height: 100vh;
}

/* Sidebar Styles */
.sidebar {
  width: 250px;
  background-color: #333;
  color: #fff;
  padding: 20px;
  box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
}

.sidebar h2 {
  margin-top: 0;
  font-size: 1.5rem;
}

.toggle-button {
  background-color: #4caf50;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 10px 15px;
  cursor: pointer;
  margin-bottom: 15px;
  width: 100%;
  text-align: left;
}

.toggle-button:hover {
  background-color: #45a049;
}

.slide-fade-enter-active, .slide-fade-leave-active {
  transition: all 0.5s ease;
}

.slide-fade-enter, .slide-fade-leave-to {
  transform: translateY(-10px);
  opacity: 0;
}

.sidebar .session-input {
  margin-top: 20px;
}

.sidebar .session-input label {
  display: block;
  margin-bottom: 8px;
  font-weight: bold;
}

.sidebar .session-input input,
.sidebar .session-input select {
  width: 100%; /* Ensure all inputs have the same width */
  padding: 10px;
  margin-bottom: 15px;
  border-radius: 5px;
  border: none;
  box-sizing: border-box; /* Ensure padding does not affect width */
}

/* Main Content Styles */
.main-content {
  flex-grow: 1;
  padding: 40px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  position: relative;
}

.timer {
  text-align: center;
  margin-bottom: 30px;
}

.timer h1 {
  font-size: 4rem;
  margin-bottom: 20px;
}

.button-group {
  display: flex;
  justify-content: center;
}

.button-group button {
  font-size: 1.5rem;
  padding: 15px 20px;
  margin: 5px;
  border: none;
  border-radius: 5px;
  background-color: #4caf50;
  color: white;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.2s;
}

.button-group button:hover {
  background-color: #45a049;
  transform: scale(1.1);
}

.button-group button i {
  pointer-events: none; /* Ensure the icon doesn't interfere with button click */
}

.history {
  margin-top: 30px;
  width: 100%;
  max-width: 600px;
}

.history h2 {
  margin-bottom: 10px;
}

.history ul {
  list-style: none;
  padding: 0;
  text-align: left;
}

.history li {
  margin: 5px 0;
  padding: 10px;
  background-color: #fff;
  border: 1px solid #ddd;
  border-radius: 5px;
}

/* Pagination Styles */
.pagination {
  display: flex;
  justify-content: space-between;
  margin-top: 10px;
}

.pagination button {
  background-color: #4caf50;
  color: white;
  border: none;
  padding: 8px 12px;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.pagination button:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.pagination button:hover:not(:disabled) {
  background-color: #45a049;
}

/* Footer Styles */
.footer {
  position: absolute;
  bottom: 0;
  width: 100%;
  text-align: center;
  padding: 10px 0;
  background-color: #f0f0f0;
  color: #100f0f;
}

.footer .social-links {
  margin-bottom: 5px;
}

.footer .social-links a {
  margin: 0 10px;
  color: #424442;
  font-size: 1.5rem;
  text-decoration: none;
  transition: color 0.3s;
}

.footer .social-links a:hover {
  color: #45a049;
}

.footer p {
  margin: 0;
  font-size: 0.9rem;
}

.footer .heart {
  color: #e25555;
  animation: heartbeat 1.5s infinite;
}

@keyframes heartbeat {
  0%, 28%, 70%, 100% {
    transform: scale(1);
  }
  14%, 42% {
    transform: scale(1.2);
  }
}
</style>
