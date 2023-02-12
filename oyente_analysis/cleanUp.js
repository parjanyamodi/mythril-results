const fs = require('fs');

const refactor = (arr) => {
    arr = arr.split('\n')
    arr = [arr[6], arr[5]]
    arr[0] = arr[0].split(": ")
    arr[1] = arr[1].split(": ")
    arr = {
        "time": arr[0][1],
        "core_usage": arr[1][1]
    }
    return arr
}

const getFile = (str) => {
    var file = fs.readFileSync(str, 'utf-8')
    return file
}


const parseIt = (file) => {
    if(file.includes("CRITICAL:root:Solidity compilation failed. Please use -ce flag to see the detail."))
    return {response: "Solidity compilation failed. Please use -ce flag to see the detail."}
    if(!file.includes("Results"))
    return {response: "No results"}
    file = file.split('\n')
    // contents = file.slice(4, 13)
    stats = file.slice(file.length-23)
    var data = {}
    // var issues = false
    for(var i = 0; i < file.length; i++) {
        var line = file[i]
        if(line.includes("Analysis Completed"))
        break;
        if(!line.includes("INFO:symExec:\t")|| line.includes("Results"))
        continue
        l = line.split(" ")
        // console.log(l)
        data[l.slice(2, l.length-2)] = l[l.length-1]
        if (l[l.length-1] !== "False") {
            data.success = true
            data.issues = [100]
        }
    };
    data = {core_usage: stats[2].split(":")[1], ...data}
    time = stats[3].split("):")[1].split(":")
    data.time = 60*parseFloat(time[0]) + parseFloat(time[1])
    // console.log(data)
    return data
}

const writeUp = (data, dir, fileName) => {
    fs.mkdirSync(`./cleaned/${dir}`, {recursive: true})
    fs.writeFileSync(`./cleaned/${dir}/${fileName}`, JSON.stringify(data, null, 4), 'utf-8')
}


const cleanUp = (str, dir, fileName) => {
    var file = getFile(str)
    if (file === undefined || file === null || file === "") {
        console.log("File not found")
        return
    }
    // console.log(dir, fileName)
    const data = parseIt(file)

    // if(data.issues.length === 0) {
    //     console.log(data)
    // }

    // Replace this
    // var unmapped = file.lastIndexOf('}')
    // var mapped = file.slice(0, unmapped + 1)
    // var remaining = file.slice(unmapped + 1)
    // var data = JSON.parse(mapped)
    // data.custom = remaining

    // console.log(data)
    writeUp(data, dir, fileName)
    // console.log("Done")
    return data
}

// cleanUp('/Users/vijayeshjeevan/Desktop/PP1/mythril-results/example.json', 'generic', 'example.json')
module.exports = cleanUp