const express = require('express');
const bodyParser = require('body-parser');
const predictRouter = require('./routes/predict');

const app = express();
app.use(bodyParser.json());

// serve static frontend if present
app.use('/', express.static('../frontend'));

app.use('/api', predictRouter);

const PORT = process.env.PORT || 3000;
app.listen(PORT, () => console.log(`Express backend listening on ${PORT}`));
