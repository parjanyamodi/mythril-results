"use strict";
const { exec } = require("child_process");

const fs = require("fs");

let rawdata = fs.readFileSync("unique.json");
let list = JSON.parse(rawdata);
const source_path = "./source_code/";
Object.values(list).map((value) => {
  console.log(value);

  exec(
    "cp " + source_path + value + " ./final_files/",
    (error, stdout, stderr) => {
      if (error) {
        console.log(`error: ${error.message}`);
        return;
      }
      if (stderr) {
        console.log(`stderr: ${stderr}`);
        return;
      }
      console.log(`stdout: ${stdout}`);
    }
  );
});
