// config/db.js
const mysql = require('mysql');
const dotenv = require('dotenv');
dotenv.config();

const connection = mysql.createConnection({
  host: process.env.DB_HOST,
  user: process.env.DB_USER,
  password: process.env.DB_PASSWORD,
  database: process.env.DB_NAME,
  port: process.env.DB_PORT
});

connection.connect((err) => {
  if (err) throw err;
  console.log('✅ Conectado a la base de datos MySQL');
});

module.exports = connection;
