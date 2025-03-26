import express from "express";
import bodyParser from "body-parser";
const app = express();

app.use(bodyParser.urlencoded({ extended: true }));

app.get("/", (req, res, next) => {
  res.send("<h1>Hello from RedeemBooks</h1>");
});

app.get("/about", (req, res, next) => {
  res.send("<h1>About us</h1><p>this is a test</p>");
});

app.post("/users", (req, res, next) => {
  res.sendStatus(201);
});

const port = 8000;
app.listen(port, () => {
  console.log(`Server running on port ${port}.`);
});
