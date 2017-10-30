const express = require('express')
const app = express()
var PythonShell = require('python-shell');
var pyshell = new PythonShell('my_script.py');

app.get('/', function (req, res) {
  res.send('NO Hello World!')
  // sends a message to the Python script via stdin
  
  pyshell.send('some value\n');
  pyshell.on('message', function (message) {
    // received a message sent from the Python script (a simple "print" statement)
    console.log(message);
  });
  
  
  // end the input stream and allow the process to exit
  // pyshell.end(function (err) {
  //   if (err) throw err;
  //   console.log('finished');
  // });
})

app.listen(3001, function () {
  console.log('Example app listening on port 3001!')
})
