//Imports modules
extractor = require("unfluff");
fs = require('fs');

//Loop over html files and extract data
fs.readdir("../html", function (err, files) {

    if (err) {
      console.error("Could not list the directory.", err);
      process.exit(1);
    }

    files.forEach(file => {
        let html_data = fs.readFileSync("../html/" + file, 'utf-8');
        let data = extractor(html_data);

        // Write data in UF directory
        fs.writeFileSync("../UF/" + file, data.text, 'utf-8')
    });
});