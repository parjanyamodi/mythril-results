const fs = require('fs');
const cleanUp = require('./cleanUp')

const processAllFiles = (dir) => {
    const types = fs.readdirSync(dir)
    types.forEach(dir => {
        fs.readdirSync(`./results/${dir}`).forEach(file => {
            cleanUp(`./results/${dir}/${file}`, dir, file)
        })
    })
}

processAllFiles('./results')