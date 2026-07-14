import sqlite3 from 'sqlite3';
import { open } from 'sqlite';
import path from 'path';

// Connect to the Python app's assistant.db located in the root project folder
const dbPath = path.resolve(process.cwd(), '../assistant.db');

export async function openDb() {
  return open({
    filename: dbPath,
    driver: sqlite3.Database
  });
}
