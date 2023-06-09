// import {readdirSync, readFile} from 'node:fs'
const { Console } = require("node:console");
const fs = require("node:fs");

const RESULTS_ROOT_DIR = "/home/kite/results/";

const FLDR_TO_VULN = {
  "swc-114": "114",
  "swc-128": "128",
  "swc-132": "132",
  "swc-134": "134",
};

const TIME_REGEX = /User time \(seconds\)\: \d+\.\d+/g;

let stats = {
  114: { time: 0, success: 0, total: 0 },
  128: { time: 0, success: 0, total: 0 },
  132: { time: 0, success: 0, total: 0 },
  134: { time: 0, success: 0, total: 0 },
};

function updateStats(resultObj, timeTaken, folder) {
  if (resultObj.error === null) {
    for (const issue of resultObj.issues) {
      if (issue["swc-id"] == FLDR_TO_VULN[folder]) {
        stats[issue["swc-id"]]["success"] += 1;
        break;
      }
    }
  }
  stats[FLDR_TO_VULN[folder]]["total"] += 1;
  stats[FLDR_TO_VULN[folder]]["time"] += timeTaken;
}

function processResults() {
  const folders = fs
    .readdirSync(RESULTS_ROOT_DIR, { withFileTypes: true })
    .filter((dirent) => dirent.isDirectory())
    .map((dirent) => dirent.name);
  for (const folder of folders) {
    const results = fs
      .readdirSync(`${RESULTS_ROOT_DIR}/${folder}`, { withFileTypes: true })
      .filter((file) => {
        return file.name.endsWith(".json");
      })
      .map((file) => {
        return file.name;
      });
    for (const result of results) {
      const resultStr = fs
        .readFileSync(`${RESULTS_ROOT_DIR}/${folder}/${result}`)
        .toString();
      // console.log(result);
      const resultSplit = resultStr.split("\n");
      // console.log(resultSplit[0]);

      let resultObj, timeTaken;
      if (resultSplit[0].includes("CRITICAL")) {
        resultObj = JSON.parse(resultSplit[1]);
      } else {
        resultObj = JSON.parse(resultSplit[0]);
      }

      for (const str of resultSplit) {
        if (str.match(TIME_REGEX)) {
          timeTaken = parseFloat(str.split(": ")[1]);
        }
      }
      updateStats(resultObj, timeTaken, folder);
    }
  }
}

processResults();
console.log(stats);
