import express from "express";
const app = express();

let port = 8000;
app.listen(port, () => {
  console.log("Server running on port ", port);
});
