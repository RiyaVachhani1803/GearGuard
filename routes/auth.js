const express = require("express");
const router = express.Router();
const pool = require("../database");
const bcrypt = require("bcrypt");
const validatePassword = require("../utils/passValidate");

//signup


router.post("/signup", async (req, res) => {
  const { name, email, password, confirmPassword } = req.body;

  if (!name || !email || !password || !confirmPassword)
    return res.status(400).json({ error: "All fields required" });

  if (password !== confirmPassword)
    return res.status(400).json({ error: "Passwords do not match" });

  const regex = /^(?=.*[a-z])(?=.*[A-Z])(?=.*[\W_]).{8,}$/;
  if (!regex.test(password))
    return res.status(400).json({ error: "Weak password" });

  const [user] = await pool.query(
    "SELECT id FROM users WHERE email = ?",
    [email]
  );

  if (user.length)
    return res.status(400).json({ error: "User already exists" });

  const hashed = await bcrypt.hash(password, 10);

  await pool.query(
    "INSERT INTO users (name, email, password) VALUES (?, ?, ?)",
    [name, email, hashed]
  );

  res.json({ message: "Signup successful" });
});

//login

router.post("/login", async (req, res) => {
  const { email, password } = req.body;

  if (!email || !password) {
    return res.render("login", {
      error: "All fields are required",
      success: null
    });
  }

  const [users] = await pool.query(
    "SELECT * FROM users WHERE email = ?",
    [email]
  );


  if (users.length === 0) {
    return res.render("login", {
      error: "Account not exist",
      success: null
    });
  }

  const user = users[0];

  const isMatch = await bcrypt.compare(password, user.password);


  if (!isMatch) {
    return res.render("login", {
      error: "Invalid Password",
      success: null
    });
  }


  return res.render("login", {
    error: null,
    success: "Login successful!"
  });
});


router.post("/forgotPass", async (req, res) => {
  const { email } = req.body;

  if (!email) {
    return res.render("forgotPass", {
      error: "Email is required",
      success: null
    });
  }

  const [users] = await pool.query(
    "SELECT id FROM users WHERE email = ?",
    [email]
  );


  if (users.length === 0) {
    return res.render("forgotPass", {
      error: "Account not exist",
      success: null
    });
  }

 
  return res.render("forgotPass", {
    error: null,
    success: "Password reset instructions have been sent to your email"
  });
});

module.exports = router;
