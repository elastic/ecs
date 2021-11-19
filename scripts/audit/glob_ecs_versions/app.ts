import {sync} from 'glob';
import {join} from 'path';
import {readFile} from 'fs';

let root: string = '/Users/djptek/github/kibana/x-pack/plugins/';
let filematches: string[] = ['*.ts', '*.tsx', '*.json', '*.tsx.snap'];
let re = /.*ecs[\W\D]*version[\W\D]*?([\d]+\.[\d]+\.[\d]+).*/;
console.log("Looking under directory %s\nfor ECS version matches in files of types %s", root, filematches.toString());
var filecount = 0;

for (let filematch of filematches) {
    let target: string = join(root, '**/', filematch);
    let filePaths: string[] = sync(target);
    filecount += filePaths.length;    
    for (let filename of filePaths) {
      readFile(filename, (err, data) => {
        if (err) throw err;
        let matches:string[] = data.toString().match(re);
        if (matches != null && matches.length >= 1) console.log("%s\t%s", matches[1], filename);
        });
    }    
}

//console.log("Looked in a total of %d files", filecount);

