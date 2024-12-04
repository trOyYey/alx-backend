import express from 'express';
import { createClient } from 'redis';
import { promisify } from 'util';
import { createQueue } from 'kue';

const client = createClient();
client.on('error', (err) => console.log(`Redis client not connected to server: ${err.message}`));
client.on('connect', () => {
  console.log('Redis client connected to the server');
});

const queue = createQueue();

const getAsync = promisify(client.get).bind(client);

const app = express();

app.use(express.json());

app.use(express.urlencoded({ extended: true }));

function reserveSeat(seats) {
  client.set('available_seats', seats);
}

async function getCurrentAvailableSeats() {
  const availableSeats = await getAsync('available_seats');
  return Number(availableSeats);
}

let reservationEnabled = true;

app.get('/available_seats', async (req, res) => {
  const availableSeats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats: availableSeats });
});

app.get('/reserve_seat', (req, res) => {
  if (!reservationEnabled) {
    res.json({ status: 'Reservation are blocked' });
    return;
  }
  const job = queue.create('reserve_seat').save((err) => {
    if (err) return res.json({ status: 'Reservation failed' });
    return res.json({ status: 'Reservation in process' });
  });
  job.on('complete', () => {
    console.log(`Seat reservation job ${job.id} completed`);
  });
  job.on('failed', (err) => {
    console.log(`Seat reservation job ${job.id} failed: ${err}`);
  });
});

app.get('/process', (req, res) => {
  queue.process('reserve_seat', async (job, done) => {
    const seats = (await getCurrentAvailableSeats()) - 1;
    reserveSeat(seats);
    if (seats === 0) {
      reservationEnabled = false;
    } else if (seats < 0) {
      return done(new Error('Not enough seats available'));
    }
    return done();
  });
  res.json({ status: 'Queue processing' });
});

app.listen(1245, () => {
  console.log('Listening on port 1245');
  reserveSeat(50);
});
