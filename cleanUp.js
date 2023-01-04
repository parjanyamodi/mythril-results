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
    var unmapped = file.lastIndexOf('}')
    var mapped = file.slice(0, unmapped + 1)
    var remaining = file.slice(unmapped + 1)
    remaining = refactor(remaining)
    var data = JSON.parse(mapped)
    data = {...data, ...remaining}
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
    console.log(dir, fileName)
    const data = parseIt(file)

    // Replace this
    // var unmapped = file.lastIndexOf('}')
    // var mapped = file.slice(0, unmapped + 1)
    // var remaining = file.slice(unmapped + 1)
    // var data = JSON.parse(mapped)
    // data.custom = remaining

    console.log(data)
    writeUp(data, dir, fileName)
    console.log("Done")
}

// cleanUp('/Users/vijayeshjeevan/Desktop/PP1/mythril-results/example.json', 'generic', 'example.json')
module.exports = cleanUp