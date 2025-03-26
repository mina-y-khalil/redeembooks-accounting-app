import express from "express";
const app = express();

app.get("/", (req, res, next) => {
  res.send("<h1>Hello from RedeemBooks</h1>");
});

app.get("/about", (req, res, next) => {
  res.send("<h1>About us</h1><p>this is a test</p>");
});

app.get("/*", (req, res, next) => {
  res.status(404);
});

const port = 8000;
app.listen(port, () => {
  console.log(`Server running on port ${port}.`);
});
