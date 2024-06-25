// Importing needed modules
import express from 'express';
import { promisify } from 'util';
import { createQueue } from 'kue';
import { createClient } from 'redis';

// Creating Express app
const app = express();
const port = 1245;

// Creating Redis client
const redisClient = createClient();

// Creating Kue queue
const queue = createQueue();

// Promisify Redis functions
const setAsync = promisify(redisClient.set).bind(redisClient);
const getAsync = promisify(redisClient.get).bind(redisClient);

// Function reserving seats
async function reserveSeat(number) {
    await setAsync('available_seats', number);
}

// Function getting current available seats
async function getCurrentAvailableSeats() {
    const availableSeats = await getAsync('available_seats');
    return availableSeats ? parseInt(availableSeats) : 0;
}

// Initialize available seats and reservationEnabled
reserveSeat(50); // Set the initial number of available seats to 50
let reservationEnabled = true; // Enable reservations initially

// Route getting available seats
app.get('/available_seats', async (req, res) => {
    const numberOfAvailableSeats = await getCurrentAvailableSeats();
    res.json({ numberOfAvailableSeats });
});

// Route to reserved seat
app.get('/reserve_seat', (req, res) => {
    if (!reservationEnabled) {
        return res.json({ status: "Reservation are blocked" });
    }
    
    const job = queue.create('reserve_seat').save(err => {
        if (err) {
            return res.json({ status: "Reservation failed" });
        }
        res.json({ status: "Reservation in process" });
    });
});

// Route to process the queue
app.get('/process', async (req, res) => {
    res.json({ status: "Queue processing" });
    
    queue.process('reserve_seat', async (job, done) => {
        const availableSeats = await getCurrentAvailableSeats();
        if (availableSeats <= 0) {
            reservationEnabled = false;
            return done(new Error("Not enough seats available"));
        }
        
        await reserveSeat(availableSeats - 1);
        if (availableSeats - 1 === 0) {
            reservationEnabled = false;
        }
        
        done();
    });
});

// Starting the server
app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});