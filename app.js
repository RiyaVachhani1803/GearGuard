require("dotenv").config();

const express = require("express");
const pool = require("./database");
const path = require("path");

const app = express();
app.use(express.json());


app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "views"));
app.use(express.static(path.join(__dirname, "public")));
app.use(express.static(path.join(__dirname, "public")));
app.use(express.urlencoded({ extended: true }));



(async () => {
  try {
    const [rows] = await pool.query("SELECT 1");
    console.log("Database connected successfully");
  } catch (err) {
    console.error("DB failed:", err);
  }
})();

const authRoutes = require("./routes/auth");
app.use("/auth", authRoutes);

app.listen(3000, () => {
  console.log("Server running on port 3000");
});

app.get("/signup", (req, res) => {
  res.render("signup", {error: null,success: null });
});

app.get("/login", (req, res) => {
  res.render("login", {error: null,success: null });
});

app.get("/forgotPass", (req, res) => {
  res.render("forgotPass", { error: null, success: null });
});

