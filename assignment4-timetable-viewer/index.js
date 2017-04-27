const http = require('http')
var fs = require('fs')
var path = require('path')
const port = 3000

const requestHandler = (request, response) => {
  console.log(request.url)
  dispatch(request, response)
}

const server = http.createServer(requestHandler)

server.listen(port, (err) => {
  if (err) {
    return console.log('something bad happened', err)
  }

  console.log(`server is listening on ${port}`)
})


function dispatch(request, response) {
    //set the base path so files are served relative to index.html
    var basePath = "app";
    var filePath = basePath + request.url;

    var contentType = 'text/html';
    var extname = path.extname('filePath');
    //get right Content-Type
    switch (extname) {
        case '.js':
            contentType = 'text/javascript';
            break;
        case '.css':
            contentType = 'text/css';
            break;
    }

    //default to index.html
    if (filePath == "app/") {
        filePath += "bus_page.html";
    }

    if (filePath === 'app/favicon.ico') {
        response.writeHead(200, {'Content-Type': 'image/x-icon'} );
        response.end();
        console.log('favicon requested');
        return;
    }

    //Write the file to response
    fs.readFile(filePath, function(error, content) {
        if (error) {
            response.writeHead(500);
            response.end();
        } else {
            response.writeHead(200, {'Content-Type': contentType});
            response.end(content, 'utf-8');
        }
});

}
