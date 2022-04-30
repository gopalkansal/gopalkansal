var express = require('express');
const bodyParser = require('body-parser');
var app = express();

app.use(bodyParser.urlencoded({ extended: true }));
app.use(express.static("public"));

app.listen(5500, function () {
    console.log('server running on port 5500');
})



app.get('/', callName);

function callName(req, res) {
    res.sendFile(__dirname + "/home.html");
    // Use child_process.spawn method from 
    // child_process module and assign it
    // to variable spawn
    // var spawn = require("child_process").spawn;

    // Parameters passed in spawn -
    // 1. type_of_script
    // 2. list containing Path of the script
    //    and arguments for the script 

    // E.g : http://localhost:3000/name?firstname=Mike&lastname=Will
    // so, first name = Mike and last name = Will

    // var process = spawn('python', ["./hello.py",
    //     "Harshit",
    //     "Goel"]);

    // Takes stdout data from script which executed
    // with arguments and send this data to res object
    // process.stdout.on('data', function (data) {
    //     res.send(data.toString());
    // })
}

app.post('/', function (req, res) {
    var spawn = require("child_process").spawn;
    console.log("Above");
    var process = spawn('python', ["./hello.py",
        req.body.Fname,
        Number(req.body.Lname)]);

    console.log(req.body.Lname);

    // process.stdout.on('data', function (data) {
    //     console.log("h1");
    //     res.send(data.toString());
    // })
    console.log("End");
    // res.redirect('/');
    // res.sendFile(__dirname + "/FCFSgraph.png");
    res.sendFile(__dirname + '/graph.html');

})


app.post("/disk", function (req, res) {
    var algo = req.body.Algo;
    if (algo === "FCFS") {
        res.sendFile(__dirname + "/fcfs.html");
    }
    else if (algo === "SSTF") {
        res.sendFile(__dirname + "/sstf.html");
    }
    else if (algo === "SCAN") {
        res.sendFile(__dirname + "/scan.html");
    }
    else if (algo === "C-SCAN") {
        res.sendFile(__dirname + "/cscan.html");
    }
    else if (algo === "LOOK") {
        res.sendFile(__dirname + "/look.html");
    }
    else if (algo === "C-LOOK") {
        res.sendFile(__dirname + "/clook.html");
    }
})

app.post("/memory", function (req, res) {
    var algo = req.body.Algo;
    if (algo === "First_FIT") {
        res.sendFile(__dirname + "/first_fit.html");
    }
    else if (algo === "Best_Fit") {
        res.sendFile(__dirname + "/best_fit.html");
    }
    else if (algo === "Worst_Fit") {
        res.sendFile(__dirname + "/worst_fit.html");
    }
    else if (algo === "Next_Fit") {
        res.sendFile(__dirname + "/next_fit.html");
    }
})

app.post("/fcfs", function (req, res) {
    var reqSeq = req.body.ReqSeq;
    var headPos = req.body.HeadPos;

    var spawn = require("child_process").spawn;

    var process = spawn('python', ["./disk.py",
        reqSeq,
        Number(headPos), "fcfs"]);

    // process.stdout.on('data', function (data) {
    //     console.log("h1");
    //     res.send(data.toString());
    // })
    // res.redirect('/');
    // res.sendFile(__dirname + "/FCFSgraph.png");
    // res.sendFile(__dirname + '/graph.html');

})

app.post("/sstf", function (req, res) {
    var reqSeq = req.body.ReqSeq;
    var headPos = req.body.HeadPos;

    var spawn = require("child_process").spawn;

    var process = spawn('python', ["./disk.py",
        reqSeq,
        Number(headPos), "sstf"]);

})

app.post("/scan", function (req, res) {
    var reqSeq = req.body.ReqSeq;
    var headPos = req.body.HeadPos;

    var spawn = require("child_process").spawn;

    var process = spawn('python', ["./disk.py",
        reqSeq,
        Number(headPos), "scan"]);

})

app.post("/cscan", function (req, res) {
    var reqSeq = req.body.ReqSeq;
    var headPos = req.body.HeadPos;

    var spawn = require("child_process").spawn;

    var process = spawn('python', ["./disk.py",
        reqSeq,
        Number(headPos), "cscan"]);

})

app.post("/look", function (req, res) {
    var reqSeq = req.body.ReqSeq;
    var headPos = req.body.HeadPos;

    var spawn = require("child_process").spawn;

    var process = spawn('python', ["./disk.py",
        reqSeq,
        Number(headPos), "look"]);

})

app.post("/clook", function (req, res) {
    var reqSeq = req.body.ReqSeq;
    var headPos = req.body.HeadPos;

    var spawn = require("child_process").spawn;

    var process = spawn('python', ["./disk.py",
        reqSeq,
        Number(headPos), "clook"]);

})

app.post("/disk_comp", function (req, res) {
    var reqSeq = req.body.ReqSeq;
    var headPos = req.body.HeadPos;

    var spawn = require("child_process").spawn;

    var process = spawn('python', ["./disk.py",
        reqSeq,
        Number(headPos), "disk_comp"]);

})

app.post("/first_fit", function (req, res) {
    var reqSeq = req.body.BlockSizes;
    var headPos = req.body.MemReq;

    var spawn = require("child_process").spawn;

    var process = spawn('python', ["./memory.py",
        reqSeq,
        headPos, "first_fit"]);

    // process.stdout.on('data', function (data) {
    //     console.log("h1");
    //     res.send(data.toString());
    // })

})

app.post("/best_fit", function (req, res) {
    var reqSeq = req.body.BlockSizes;
    var headPos = req.body.MemReq;

    var spawn = require("child_process").spawn;

    var process = spawn('python', ["./memory.py",
        reqSeq,
        headPos, "best_fit"]);

})

app.post("/worst_fit", function (req, res) {
    var reqSeq = req.body.BlockSizes;
    var headPos = req.body.MemReq;

    var spawn = require("child_process").spawn;

    var process = spawn('python', ["./memory.py",
        reqSeq,
        headPos, "worst_fit"]);

})

app.post("/next_fit", function (req, res) {
    var reqSeq = req.body.BlockSizes;
    var headPos = req.body.MemReq;

    var spawn = require("child_process").spawn;

    var process = spawn('python', ["./memory.py",
        reqSeq,
        headPos, "next_fit"]);

})

app.post("/memory_comp", function (req, res) {
    var reqSeq = req.body.BlockSizes;
    var headPos = req.body.MemReq;

    var spawn = require("child_process").spawn;

    var process = spawn('python', ["./memory.py",
        reqSeq,
        headPos, "memory_comp"]);

    // process.stdout.on('data', function (data) {
    //     console.log("h1");
    //     res.send(data.toString());
    // })

})

app.post("/backToHome", function (req, res) {
    res.redirect('/');
})

app.post('/ind', function (req, res) {
    res.redirect('/');
})

app.post('/graph', function (req, res) {
    res.sendFile(__dirname + "/graph.html");
})